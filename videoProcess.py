from io import StringIO
import cv2

import config
import textProcess
import helper

# converts an image to ANSI color escape codes
def imToTextColor(img, frames, colorReduction):
    rows, cols, _ = img.shape
    output = StringIO() 

    img = (img // colorReduction) * colorReduction
    last_color = [0, 0, 0]

    for i in range(rows):
        for j in range(cols):
            color = list(img[i, j])

            if last_color != color or j == 0:
                output.write(f"\033[48;2;{color[2]};{color[1]};{color[0]}m  ")
            else:
                output.write("  ")
            last_color = color
        output.write("\n")
    output.write("\n")
    frames.append(output.getvalue())  # add frame to frames array


# converts an image to ASCII
def imToText(img, frames):
    rows, cols, _ = img.shape
    output = StringIO()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightValues = ["  ", "- ", "= ", "o ", "O ", "0 ", "% ", "@ "]

    # iterate through the pixels and check brightness against the brightValues list
    for i in range(rows):
        for j in range(cols):
            color = img[i, j]
            output.write(brightValues[color // 32])
        output.write("\n")

    output.write("\n")
    frames.append(output.getvalue())  # add frame to frames array


#get the "difference" between two frames, or in other words, the print needed
#to transition from the "last" frame to the "current" frame
def getDifference(current, last, color):
    output = StringIO() #use stringIO for speeeeeeeed

    cLines = current.split("\n")
    lLines = last.split("\n")

    for i in range(len(cLines)):
        if cLines[i] == lLines[i]:
            output.write("\n")
        else:
            output.write(textProcess.getLineDiff(cLines[i], lLines[i], color))

    return output.getvalue()


# processes a video into either pure text or color
def processVideo(v, logger = None):
    is_grabbed, frame = v.cap.read()

    # scale down image based on size
    scale_percent = (
        v.size / frame.shape[0]
        if v.resizeToHeight
        else v.size / frame.shape[1]
    )
    dim = (int(frame.shape[1] * scale_percent), int(frame.shape[0] * scale_percent))

    count = 0
    while is_grabbed:  # iterate through all frames
        is_grabbed, frame = v.cap.read()

        if logger:
            c = (count / v.skip) if v.skip else count
            logger(c/v.frameCount, c, v.frameCount, )

        # skips frames based on the skip variable... i dont know why i added this comment
        if v.skip and count % v.skip == 0:
            count += 1
            continue

        # resize and convert to text
        if is_grabbed:
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            
            if v.color:
                imToTextColor(frame, v.frames, v.colorReduction)
            else:
                imToText(frame, v.frames)

            if v.skip and count % v.skip != 0 and len(v.frames) > 1:
                v.frameDiffs.append(getDifference(v.frames[len(v.frames) - 1], v.frames[len(v.frames) - 2], v.color))
            elif len(v.frames) > 1:
                v.frameDiffs.append(getDifference(v.frames[len(v.frames) - 1], v.frames[len(v.frames) - 2], v.color))
            elif len(v.frames) == 1:
                v.frameDiffs.append(v.frames[0])
        else:
            break
        count += 1

    v.cap.release()
