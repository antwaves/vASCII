from pydub import AudioSegment
import config


# takes the video and creates a new mp3 file
def loadAudio(path):
    video = AudioSegment.from_file(path, format=config.videoExt)
    video.export(f"{config.audioFolder}\\{config.videoStr}.{config.audioExt}", format=config.audioExt)


# plays audio. ad
def playAudio():
    if not playback.active:
        playback.load_file(path_to_file=f"{config.audioFolder}\\{config.videoStr}.{config.audioExt}")

    if playback.paused:
        playback.resume()
    else:
        playback.play()


#pause the audioooo
def pauseAudio():
    if not playback.active:
        playback.load_file(path_to_file=f"{config.audioFolder}\\{config.videoStr}.{config.audioExt}")
    playback.pause()
