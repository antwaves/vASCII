from io import StringIO
from pathlib import PurePath

from .audio import loadFromHex

# encode a video into text
def encodeVideo(raw_path: str, video, logger=None) -> None:
    path = PurePath(raw_path)

    with open(f"{path}", "w") as f:
        f.write(f"{video.color} {video.fps} {len(video.frameDiffs)}\n")

        skips = 0
        count = 0

        for frame in video.frameDiffs:
            compressed = StringIO()

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
            f.write(
                "\\\n" if not video.color else "\\\\\n"
            )  # write a different frame seperator based on color

            if logger:
                percent = count / video.frameCount if count == 0 else 0
                logger(percent, count, video.frameCount)
            count += 1

        if video.audioData:
            f.write("\\\\\\\n")
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
        lines.pop(0)

        currentFrameCount = 0
        currentLineCount = 0

        currentFrame = StringIO()
        breakCheck = "\\\n" if not color else "\\\\\n"
        audioBreakCheck = "\\\\\\\n"

        for line in lines:
            if line == audioBreakCheck:
                hexString = lines[currentLineCount + 2].strip()
                outputString = lines[currentLineCount + 1].strip()
                video.audioOutputPath = outputString
                loadFromHex(hexString, outputString)
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
                with open("log.txt", "a") as f:
                    f.write(currentFrame.getvalue())
                    
                frames.append(currentFrame.getvalue())
                currentFrame = StringIO()

                if logger:
                    percent = currentFrameCount / totalFrameCount if currentFrameCountcount == 0 else 0
                    logger(percent, currentFrameCount, totalFrameCount)
                
                currentFrameCount += 1
            currentLineCount += 1

    video.frameDiffs = frames
    video.color = color
    video.fps = fps
    video.frameTime = 1 / fps
