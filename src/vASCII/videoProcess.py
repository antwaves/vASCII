from io import StringIO

import cv2
from . import textProcess
from .constants import *

# converts an image to ANSI color escape codes
def imToTextColor(img, frames, colorReduction):
    rows, cols, _ = img.shape
    output = StringIO()

    if colorReduction != COLOR_REDUCTION_NONE:
        img = (img // colorReduction) * colorReduction

    last_color = [0, 0, 0]

    for i in range(rows):
        for j in range(cols):
            color = tuple(img[i, j])

            if last_color != color or j == 0:
                output.write(f"\033[48;2;{color[2]};{color[1]};{color[0]}m  ")
            else:
                output.write("  ")
            last_color = color
        output.write("\n")
        
    output.write("\n")
    frames.append(output.getvalue())  # add frame to frames array

# converts an image to ASCII
def imToText(img, charSet: list, frames: list, exceptionHandler) -> None:
    output = StringIO()

    try:
        rows, cols = img.shape
    except ValueError:
        rows, cols, _ = img.shape
    chars = [char + " " for char in charSet]

    if 256 % len(charSet) == 0:
        div = int(256 / len(charSet))
    else:
        raise exceptionHandler("Invalid character set provided")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # iterate through the pixels and check brightness against charset
    for i in range(rows):
        for j in range(cols):
            color = img[i, j]
            output.write(chars[color // div])
        output.write("\n")

    output.write("\n")
    frames.append(output.getvalue())  # add frame to frames array

# get the "difference" between two frames, or in other words, the print needed
# to transition from the "last" frame to the "current" frame
def getDifference(current, last, color):
    output = StringIO()  # use stringIO for speeeeeeeed

    cLines = current.split("\n")
    lLines = last.split("\n")

    for i in range(len(cLines)):
        if cLines[i] == lLines[i]:
            output.write("\n")
        else:
            output.write(textProcess.getLineDiff(cLines[i], lLines[i], color))

    return output.getvalue()


''' 
NOTE TO SELF
Change how this works, feed the image data directly to a 
difference function and THEN turn the data into text. 
Final output shouldnt change the export/import
'''
# processes a video into either pure text or color
def processVideo(v, exceptionHandler, logger=None):
    count = 0
    while True:  # iterate through all frames
        is_grabbed, frame = v.videoCap.read()

        if not is_grabbed and count == 0:
            exceptionHandler("VideoMissingError: Could not open video")
        elif not is_grabbed:
            break

        if logger:
            actualFrameNumber = (count / v.skip) if v.skip else count
            logInfo = {"currentFrameNumber": actualFrameNumber, 
                       "frameCount": v.frameCount, 
                       "percentComplete": actualFrameNumber / v.frameCount}
            logger(logInfo)

        if v.skip and count % v.skip == 0:
            count += 1
            continue

        # resize and convert to text
        if is_grabbed:
            if v.width and v.height:
                frame = cv2.resize(frame, (int(v.width), int(v.height)), interpolation=cv2.INTER_AREA)

            if v.color:
                imToTextColor(frame, v.frames, v.colorReduction)
            else:
                imToText(frame, v.charSet, v.frames, exceptionHandler)

            if v.skip and count % v.skip != 0 and len(v.frames) > 1:
                v.frameDiffs.append(
                    getDifference(
                        v.frames[len(v.frames) - 1],
                        v.frames[len(v.frames) - 2],
                        v.color,
                    )
                )
            elif len(v.frames) > 1:
                v.frameDiffs.append(
                    getDifference(
                        v.frames[len(v.frames) - 1],
                        v.frames[len(v.frames) - 2],
                        v.color,
                    )
                )
            elif len(v.frames) == 1:
                v.frameDiffs.append(v.frames[0])            
        count += 1
