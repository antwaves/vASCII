from io import StringIO
from pathlib import PurePath

from .audio import loadFromHex


'''
A video is encoded as such within a text file:

Video Header
Frame Data
Audio Data (optional)

The video header contains whether the video is in color, the fps, the total frame number, the width and the height. 
This is all the first line of a file, seperated by spaces, and in the order mentioned above. All the above values are ints, except for color,
where a true value is repersented as the string True, and a false value is repersented as the string False
The header values are stored as strings (then casted to a bool/int). Things like frametime, and video length are derived from these values
All values in the header are necessary for display as a video, but said values are not necessarily needed for display within a terminal

The frame data contains all frames within a video, and is put directly after the header
Individual frames are first compressed skipping unecessary parts of ASCII commands (that are only used in printing)
There are two types of ASCII commands used, color commands, and cursor moving commands
Color Set Command: \033[48;2;{color[2]};{color[1]};{color[0]}m  
Cursor Move Command: \033[{moveAmount}C
To compress these commands, we first check if the command is a color set. If so, we remove "[48;2;"
Then, we check if it a cursor move. If so, we remove "["
Then we throw away extra spaces that are used in printing, since each "pixel" is two characters wide and one character high
Each individual frame is seperated with a "\" (note, that due to the nature of backslashes, this apears as \\ in code)

The audio data contains the entire audio track for the video, and is put directly after the frame data
The audio track is put into a hexadecimal format, then converted to a string, and put all on one line
The start of the audio data is specified with a "\\" (note, that due to the nature of backslashes, this appears as "\\\\" in code)
'''

# encode a video into text
def encodeVideo(raw_path: str, video, logger=None) -> None:
    path = PurePath(raw_path)

    with open(f"{path}", "w") as f:
        f.write(f"{video.color} {video.fps} {len(video.frameDiffs)} {video.width} {video.height}\n")

        skips = 0
        count = 0

        for frame in video.frameDiffs:
            compressed = StringIO()

            #see above comment for any magic numbers here
            for i in range(len(frame)): 
                if skips > 0:
                    skips -= 1
                    continue

                if frame[i] == "\033" and frame[i + 2] == "4" and frame[i + 4] == ";":
                    skips += 6

                elif frame[i] == "\033":
                    skips += 1

                if frame[i] != "\n" and frame[i + 1] == " ":
                    skips += 1

                compressed.write(frame[i])

            f.write(compressed.getvalue())
            f.write("\\\n")

            if logger:
                logInfo = {"currentFrameNumber": count, 
                        "frameCount": video.frameCount, 
                        "percentComplete": count / video.frameCount}
                logger(logInfo)
            count += 1

        if video.audioData:
            f.write("\\\\\n")
            f.write(str(PurePath(video.audioOutputPath)) + '\n')
            f.write(str(video.audioData))

        f.close()


# decode text into a video
def decodeVideo(raw_path, video, logger=None) -> None:
    frames = []

    path = PurePath(raw_path)
    with open(path, "r") as f:
        lines = f.readlines()
        info = lines[0].split()

        color = False if info[0] == "False" else True
        fps = int(float(info[1]))
        totalFrameCount = int(info[2])
        width = int(info[3])
        height = int(info[4])

        lines.pop(0)

        currentFrameCount = 0
        currentLineCount = 0

        currentFrame = StringIO()
        breakCheck = "\\\n"
        audioBreakCheck = "\\\\\n"

        for line in lines:
            if line == audioBreakCheck:
                hexString = lines[currentLineCount + 2].strip()
                outputString = lines[currentLineCount + 1].strip()
                video.audioOutputPath = outputString
                loadFromHex(hexString, outputString)
                video.audioData = hexString
                break

            elif line != breakCheck:
                skips = 0

                for i in range(len(line)):
                    char = line[i]

                    if skips > 0:
                        skips -= 1
                        continue

                    if char == "\033":
                        j = i
                        temp = line[j]
                        outTemp = StringIO()
                        currentFrame.write(char + "[")

                        while temp != "C" and temp != "m":
                            j += 1
                            skips += 1
                            temp = line[j]
                            outTemp.write(temp)

                        if temp == "m":
                            currentFrame.write("48;2;")
                        
                            if line[j + 1 == ' ']:
                                outTemp.write(' ')

                        currentFrame.write(outTemp.getvalue())
                        continue

                    if char == "\n":
                        currentFrame.write(char)
                        continue
                    
                    if line[i + 1] == "\033":
                        currentFrame.write(char)
                        continue

                    currentFrame.write(char + " ")
            else:  
                frames.append(currentFrame.getvalue())
                currentFrame = StringIO()
                
                if logger:
                    logInfo = {"currentFrameNumber": currentFrameCount, 
                            "frameCount": totalFrameCount, 
                            "percentComplete": currentFrameCount / totalFrameCount}
                    logger(logInfo)
                        
                currentFrameCount += 1
            currentLineCount += 1

    video.frameDiffs = frames
    video.color = color

    video.fps = fps
    video.length = fps / totalFrameCount
    video.frameTime = 1 / fps

    video.width = width
    video.height = height
    