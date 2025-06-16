videoStr = "taxes"  # the filename of the video
videoExt = "mp4"  # the file extension of the video
videosFolder = "videos"  # the folder in which videos are contained
audioFolder = "audio"  # the folder in which audio to be played is placed into
audioExt = "mp3"  # the file extension of the audio. internal, should not be changed by the user.

exporting = True #whether or not exporting
importing = False #whether or not importing
importStr = "taxes" #name of import file

size = 100 # sets the size of one of the axises of the video (downscaled is recommended)
resizeToHeight = False  # if True, width is resized to the ratio of height (which will be set to the size variable), and vice versa if False

fpsLimit = 12  # limits fps to avoid lag. set to None if you don't want to limit fps
colorReduction = 16  # (256/colorReduction)^3 = amount of possible colors on the screen
mute = False  # If True, audio is muted, else, audio plays
color = False # if True, ANSI escape codes are used to add color to the image, if False, pure ASCII is used. not recommended for larger sizes

loadingBar = True  # if True, loading bar is shown, if False, it isnt
