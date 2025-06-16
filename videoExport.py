from io import StringIO
import helper

#encode a video into text
def encodeVideo(frames: list, filename: str, fps: int, color: bool) -> None:
    with open(f"{filename}.txt", 'w') as f:
        f.write(f"{filename} {color} {fps}\n")
        f.close()

    with open(f"{filename}.txt", 'a') as f:
        skips = 0
        count = 0

        for frame in frames:
            compressed = StringIO()
            
            for i in range(len(frame)):
                if skips > 0:
                    skips -= 1
                    continue

                if frame[i] == '\033' and frame[i + 2] == '4' and frame[i + 4] == ';':
                    skips += 6

                elif frame[i] == '\033':
                   skips += 1

                if frame[i] != "\n" and frame[i + 1] == " ":
                    skips += 1
                              
                compressed.write(frame[i])

            f.write(compressed.getvalue())
            f.write("\\\n" if not color else "\\\\\n") #write a different frame seperator based on config.color

            count += 1  
            if count % 50 == 0:
                helper.ieLog("exported", count, fps)
        f.close()
    
    helper.ieLog("exported", count, fps)
    print("")
    
    
#decode text into a video
def decodeVideo(filename):
    frames = []

    with open(f"{filename}.txt", 'r') as f:
        lines = f.readlines()
        info = lines[0].split()
        filename, color, fps = info[0], False if info[1] == "False" else True, int(float(info[2])) #get the config info
        lines.pop(0)
        f.close()

    #write the dumb frames
    with open(f"{filename}.txt", 'r') as f:
        count = 0
        currentFrame = StringIO()
        breakCheck = "\\\n" if not color else "\\\\\n"

        for line in lines:
            if line != breakCheck:
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
                        currentFrame.write(char + '[')

                        while temp != "H" and temp != "C" and temp != "m":
                            j += 1
                            skips += 1
                            temp = line[j]
                            outTemp.write(temp)   

                        if temp == "m":
                            currentFrame.write("48;2;")
                        
                        currentFrame.write(outTemp.getvalue())
                        continue
                        
                    if char == '\n':
                        currentFrame.write(char)
                        continue

                    if line[i + 1] == '\033':
                        currentFrame.write(char)
                        continue

                    currentFrame.write(char + " ")
            else:
                with open("log.txt", "a") as f:
                    f.write(currentFrame.getvalue())

                frames.append(currentFrame.getvalue())
                currentFrame = StringIO()

                count += 1  
                if count % 50 == 0:
                    helper.ieLog("imported", count, fps)
    
    helper.ieLog("exported", count, fps)
    print("")
    return frames, [filename, color, fps]
