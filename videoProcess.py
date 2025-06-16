from io import StringIO
import cv2

import config
import textProcess
import helper

# converts an image to ANSI color escape codes
def imToTextColor(img, frames):
    rows, cols, _ = img.shape
    output = StringIO()
    output.write(
        "\033[H"
    )  # add ANSI escape code to move cursor to top left of the screen for printing

    img = (img // config.colorReduction) * config.colorReduction
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
    output.write("\033[H")  # add ANSI escape code to move cursor to top left of the screen for printing

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
def getDifference(current, last):
    output = StringIO() #use stringIO for speeeeeeeed
    output.write("\033[H") #add the thing that moves the cursor to the top

    cLines = current.split("\n")
    lLines = last.split("\n")

    for i in range(len(cLines)):
        if cLines[i] == lLines[i]:
            output.write("\n")
        else:
            output.write(textProcess.getLineDiff(cLines[i], lLines[i], config.color))

    return output.getvalue()


# processes a video into either pure text or color
def processVideo(cap, frames, frameDiffs, frameCount):
    is_grabbed, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)

    if config.fpsLimit and fps > config.fpsLimit:
        skip = fps // config.fpsLimit

    # scale down image based on config.size
    scale_percent = (
        config.size / frame.shape[0]
        if config.resizeToHeight
        else config.size / frame.shape[1]
    )
    dim = (int(frame.shape[1] * scale_percent), int(frame.shape[0] * scale_percent))

    count = 0
    helper.log(0, frameCount, skip=skip)
    while is_grabbed:  # iterate through all frames
        is_grabbed, frame = cap.read()

        if count % 100 == 0:
            helper.log(count, frameCount, skip=skip)

        # skips frames based on the skip variable... i dont know why i added this comment
        if skip and count % skip == 0:
            count += 1
            continue

        # resize and convert to text
        if is_grabbed:
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            if config.color:
                imToTextColor(frame, frames)
            else:
                imToText(frame, frames)

            if skip and count % skip != 0 and len(frames) > 1:
                frameDiffs.append(getDifference(frames[len(frames) - 1], frames[len(frames) - 2]))
            elif len(frames) > 1:
                frameDiffs.append(getDifference(frames[len(frames) - 1], frames[len(frames) - 2]))
            elif len(frames) == 1:
                frameDiffs.append(frames[0])
        else:
            break
        count += 1

    cap.release()
    helper.log(count, frameCount, lastFrame=True)
