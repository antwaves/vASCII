# vASCII 
Creating videos and images using ASCII characters and ANSII color codes.

## Useful Stuff
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Contributing](#contributing)
- [License](#license)

# Description
vASCII converts videos or images into ASCII text or ANSII color codes, and is made primarily for the terminal. You can
- Display videos/images in both grayscale ASCII art and color
- Print videos in sync to the orginal audio, while leaving your main thread alone
- Import/Export videos for faster load times, storing them in .txt files
- Limit the size, framerate, and colors of a given video/image
- Set custom character sets
- Set a custom logger


# Requirements
- Python 3.7+
- FFmpeg installed on your system
- A terminal that accepts [ANSII cursor move commands](https://en.wikipedia.org/wiki/ANSI_escape_code) and [truecolor commands](https://github.com/termstandard/colors)


# Installation
Installation should be easy enough
```
pip install vASCII
```

or, if you want to build from source
```
git clone https://github.com/antwaves/vASCII.git
```

Thats's it. Just remember to have ffmpeg and python installed. If you need to do that, look below


#### Windows
```
choco install ffmpeg
choco install python3
```

#### Ubuntu/Debian
```
sudo apt-get update
sudo apt-get install -y build-essential python3-dev ffmpeg
```

#### macOS
```
brew install ffmpeg
```

# Quickstart
- [Videos](#videos)
- [Images](#images)
- [Importing/Exporting](#importingexporting)
- [Logging](#logging)
- [Other](#other)

## Videos
Create a video object
```py
import vASCII

v = vASCII.Video()
```

Set your preferences, if you have any

```py
#whether or not the video will be printed with ASCII or in color. Off by default, as it does decrease performance
v.color = False

#whether or not the video will be muted. Off by default
v.mute = True

#the fps limit for the video. Set to none if you dont want a limit. 12 by default
v.fpsLimit = 12 

#only applies if color is on. Limits the amount of colors for optimization. 
#possible reductions include
# COLOR_REDUCTION_NONE
# COLOR_REDUCTION_LIGHT
# COLOR_REDUCTION_NORMAL (default)
# COLOR_REDUCTION_STRONG
v.colorReduction = vASCII.COLOR_REDUCTION_STRONG 

#only applies if color is off. sets the characters used in printing
#if creating a custom set, make sure that the characters that take up the least space are at the front
#and also make sure that each list element is only one character long
v.charSet = [" ", "*", "X", "@"] 

#sets the path that any potential audio will be sent to. output.mp3 by default
v.audioOutputPath = "output.mp3"
```

Load your video file
```py
v.from_file("path/to/file.mp4")
```

Limit width/height (so the video fits in a terminal)
```py
#enter a set of dimensions (width, height) for the video to be limited to
#anything above 500, 500 is not recommended for performance
#this function will preseve aspect ratio 
v.fit_to_dim(150, 150)
```

Load your frames
```py
#this will take a while!
v.load_frames()
```

Zoom out with your terminal 'ctrl' + '-' and start!
```py
v.start_video() #runs in a different thread
```

Pause, unpause, and stop
```py
v.pause() #these will also pause audio
v.unpause() #if it is playing
v.flip_pause() #this function unpauses if the video is paused, and vice versa

v.stop() #stop the printing
```

## Images
Create an image object
```py
import vASCII

i = vASCII.Image()
```

Set your preferences, if you have any

```py
#whether or not the video will be printed with ASCII or in color. Off by default
i.color = False

#only applies if color is off. sets the characters used in printing
#if creating a custom set, make sure that the characters that take up the least space are at the front
#and also make sure that each list element is only one character long
i.charSet = [" ", "*", "X", "@"] 
```

Load your image file
```py
i.from_file("path/to/your/image.png")
```
Limit width/height (so the image fits in a terminal)
```py
#enter a set of dimensions (width, height) for the image to be limited to
#this function will preseve aspect ratio 
i.fit_to_dim(400, 400)
```
Load your text, zoom out in your terminal with "ctrl" + "-", and print
```py
i.load_text()
i.print_image()
```

## Importing/Exporting
First, export your video. If there's audio, it will also be exported
```py
import vASCII

v = vASCII.Video()

v.from_file("path/to/your/file.mp4")
v.fit_to_dim(300, 300)
v.load_frames()

v.export(path="output.txt") #no need to pass path. by default, it's output.txt
```

Now, later, let's import it
```py
v = Video()

v.from_import("output.txt")
v.start() #prints the video!
```

The main benefit of this is load time. Beware, the more detailed and the longer a video is, the larger the text file will be. Make sure you aren't creating a 2 Gigabyte behemoth (unless you want that). 

## Logging
You can pass a custom logger to three functions ```load_frames```, ```export_video```, and ```from_import```. 

First, let's make a log function. It will receive a dictionary with three values. (I know theres a better way to do this. I dont care.)

```py
def log(logInfo: dict) -> None:
    currentFrame = logInfo["currentFrameNumber"]
    totalFrameCount = logInfo["frameCount"]
    percent = logInfo["percentComplete"]

    #do log stuff here
```
Next, let's use it
```py
import vASCII

#setup
v = vASCII.Video()
v.from_file("path/to/your/file.mp4")
v.fit_to_dim(300, 300)

v.load_frames(logger=log) #replace log with the name of your function
#or v.export_video(logger=log)
#or v.from_import(path="text_file.txt", logger=log)
```

## Other
You can check if your video/image currently fits in the terminal

```py
if video.fits_in_term():
    print("It fits!")

if image.fits_in_term():
    print("It also fits!")

#fits_in_term returns a bool
```

You can manually set the width/height of a video while not preserving aspect ratio
```py
width = 200
height = 200

video.from_file("path/to/file", (width, height))
image.from_file("path/to/file", (width, height))
```

You can print a video and block the current thread until it finishes  by using ```print_video``` instead of ```start```
```py
video.start() #creates a new thread
video.print_video() #blocks current thread
```

# Contributing
Contributions are welcome! I'd be happy to receive any. Anything from code quality, optimizations, and new features is welcome. Don't be shy!

## How to contribute
1. Fork [vASCII](https://github.com/antwaves/vASCII) on github
2. Commit any changes
3. Send a pull request

You did it! Please be sure to keep your pull requests limited to one topic, and include descriptions.


# License
Copyright © 2025 antwaves

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.