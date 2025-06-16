import config
import videoExport


#validate if input is valid
def inputValidate(string: str, inputType: type):
    string = string.lower()

    if inputType == bool:
        return string == "y" or string == "n"
    elif inputType == int:
        return string.isnumeric()
    elif inputType == str:
        return string.isascii() and string.isprintable() and string != ""


#grab a type of input with a given prompt
def uInput(text: str, inputType: type = bool, tabs: int = 0):
    result = ""
    typeIndicator = ""

    if inputType == bool:
        typeIndicator = "[y/n]"
    elif inputType == int:
        typeIndicator = "[0-9]"
    elif inputType == str:
        typeIndicator = "[a-z]"

    while not inputValidate(result, inputType):
        result = input(f"{'\t' * tabs}{text} {typeIndicator}: ")

    if inputType == bool:
        return result == "y"
    elif inputType == int:
        return int(result)
    elif inputType == str:
        return result


#annoying code that grabs a bunch of config stuff
def grabInput(redo=False):
    edit = uInput("Do you want to edit config?") if not redo else True
    info = False

    if edit:
        config.importing = uInput("Do you want to import a video?", tabs=1)
        if config.importing:
            config.exporting = False
            info = videoExport.decodeVideo(uInput("Enter the filename", inputType=str, tabs=2))
            config.videoStr, config.color = info[1][0], False if info[1][1] == "False" else True

        else:
            config.exporting = uInput("Do you want to export the video?", tabs=1)


    if edit and uInput("Do you want to edit video attributes?", tabs=1):
        if not config.importing:
            config.color = uInput("Do you want to print with color?", tabs=2)
            if config.color:
                config.colorReduction = uInput("Set a color reduction, default is 16. Higher reduction means faster prints.", inputType=int,tabs=3)

            config.resizeToHeight = uInput("The video will be downscaled, select y to resize to height, and n to resize to width", tabs=2)
            config.size = uInput("Enter a size for the video that is smaller than the video's size", inputType=int, tabs=3)

            config.fpsLimit = uInput("Enter a fps limit for the video that is less than the video's fps", inputType=int, tabs=2)

        config.mute = uInput("Do you want to mute the video?", tabs=2)
        config.loadingBar = uInput("Do you want to see a loading bar?", tabs=2)


    if edit and uInput("Do you want to edit filenames?", tabs=1):
        config.videoStr = uInput("Enter the name of the file, not including the extension. For example, myVideo", inputType=str, tabs=2)
        config.videoExt = uInput("Enter the extension of the video file, not including the dot. For example, mp4", inputType=str, tabs=2)
        config.videosFolder = uInput("Enter the folder in which your video is placed. Make sure the folder is in the script directory. For example, videos", inputType=str, tabs=2)
        if not config.mute:
            config.audioFolder = uInput("Enter the folder in which the audio is to be placed. Make sure the folder is in the script directory. For example, audio", inputType=str, tabs=2)
        

    if edit and uInput("Do you want to change the settings again?"):
        grabInput(redo=True) #do recusrive stuff if rechanging settings

    return info
