from pathlib import PurePath
from io import StringIO
import cv2


class ImageError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class Image:
    def __init__(self):
        self.color = False
        self.textData = None
        self.charSet = [" ", "'", ":", ",", "-", "^", '"', "<", "c", "o", "O", "B", "W", "0", "%", "@"]

        #implement later
        self.width = None
        self.height = None


    def from_file(self, raw_path):
        path = PurePath(raw_path)
        color = cv2.IMREAD_COLOR if self.color else cv2.IMREAD_GRAYSCALE
        img = cv2.imread(path, color)

        output = StringIO()
        rows, cols = img.shape
        chars = [char + " " for char in self.charSet]

        if 256 % len(self.charSet) == 0:
            div = int(256 / len(self.charSet))
        else:
            raise imageError

        for i in range(rows):
            for j in range(cols):
                color = img[i, j]
                output.write(chars[color // div])
            output.write("\n")

        output.write("\n")

        self.textData = output.getvalue()
    
