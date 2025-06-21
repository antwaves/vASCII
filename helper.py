import config

def log(percent, count, frameCount):  # log stuff. remove if needed
    if count % 50 != 0:
        return None

    # print progress bard
    percentTw = int(percent * 20)
    print(
        f"[{'@' * percentTw}{'-' * (20 - percentTw)}] {int(count)} frames completed out of estimated {frameCount}. {int(percent * 100)}% complete",
        end="\r",
    )
