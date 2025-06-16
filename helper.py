import config

def log(count, frameCount, lastFrame=False, skip=None):  # log stuff. remove if needed
    frameCount = int(frameCount)

    if config.loadingBar:
        if lastFrame:  # deal with edge case
            print(f"[{'@' * 20}] {frameCount} frames completed out of {frameCount} frames. 100% complete")
            return None  # exit

        # deal with skipped frames
        if skip:
            count /= skip
        percent = count / frameCount

        # print progress bard
        percentTw = int(percent * 20)
        print(
            f"[{'@' * percentTw}{'-' * (20 - percentTw)}] {int(count)} frames completed out of estimated {frameCount}. {int(percent * 100)}% complete",
            end="\r",
        )

def ieLog(text: str, count: int, fps: int) -> None:
    print(f"{count} frames {text}. {int(count // fps)} seconds of video processed.", end = "\r")
