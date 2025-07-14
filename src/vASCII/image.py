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
    
        self.img = None
        self.width = None
        self.height = None
    

    def load_image(self, path: str, dimensions: tuple[int, int] = None) -> None:
        path = PurePath(path)
        img_color = cv2.IMREAD_COLOR if self.color else cv2.IMREAD_GRAYSCALE
        img = cv2.imread(path, img_color)

        if img is not None: #can't just check as a bool because this is an array
            if dimensions:
                img = cv2.resize(img, dimensions, interpolation=cv2.INTER_AREA)
            self.img = img
        else:
            raise ImageError("Image could not be loaded!")
        
        try:
            self.height, self.width, _ = self.img.shape
        except ValueError:
            self.height, self.width = self.img.shape

    #allows for resizing to fit within set dimensions while keeping aspect ratio 
    def fit_to_dim(self, dimensions: tuple[int, int]) -> None: 
        if self.width > dimensions[0]:
            scale_percent = (dimensions[0] / self.width)
            self.width = int(self.width * scale_percent)
            self.height = int(self.height * scale_percent)

        if self.height > dimensions[1]:
            scale_percent = (dimensions[1] / self.height)
            self.width = int(self.width * scale_percent)
            self.height = int(self.height * scale_percent)
        
        self.img = cv2.resize(self.img, (self.width, self.height), interpolation=cv2.INTER_AREA)


    def load_text(self) -> None:
        output = StringIO()

        if not self.color:
            chars = [char + " " for char in self.charSet]
            if 256 % len(self.charSet) == 0:
                div = int(256 / len(self.charSet))
            else:
                raise imageError("Invalid character set")
        else:
            last_color = [0, 0, 0]

        for i in range(self.height):
            for j in range(self.width):
                if not self.color:
                    color = self.img[i, j]
                    output.write(chars[color // div])
                else:
                    color = tuple(self.img[i, j])
                    if last_color != color or j == 0:
                        output.write(f"\033[48;2;{color[2]};{color[1]};{color[0]}m  ")
                    else:
                        output.write("  ")
                    last_color = color

            output.write("\n")
        output.write("\n")
        
        self.textData = output.getvalue()
    

    def print_image(self) -> None:
        print(self.textData, "\033[39m\033[49m", sep="")
    
    
    def fits_in_term(self) -> bool:
        term_size = os.get_terminal_size()
        
        if term_size:
            return term_size.columns > self.width * 2 and term_size.lines > self.height
        else:
            raise ImageError("Terminal size could not be acessed")
