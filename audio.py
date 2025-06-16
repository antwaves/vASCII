import moviepy
import config


# takes the video and creates a new mp3 file
def loadAudio(path):
    clip = moviepy.AudioFileClip(path)
    clip.write_audiofile(f"{config.audioFolder}\\{config.videoStr}.mp3", logger=None) 
    clip.close()


# plays audio. ad
def playAudio(playback):
    if not playback.active:
        playback.load_file(path_to_file=f"{config.audioFolder}\\{config.videoStr}.{config.audioExt}")

    if playback.paused:
        playback.resume()
    else:
        playback.play()

#pause the audioooo
def pauseAudio(playback):
    if not playback.active:
        playback.load_file(path_to_file=f"{config.audioFolder}\\{config.videoStr}.{config.audioExt}")
    playback.pause()
