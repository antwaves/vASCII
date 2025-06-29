from pydub import AudioSegment
from pathlib import PurePath

# takes the video and creates a new mp3 file
def loadAudio(video, raw_input_path: str, raw_output_path: str, video_format: str):
    input_path = PurePath(raw_input_path)
    output_path = PurePath(raw_output_path)

    videoData = AudioSegment.from_file(input_path, format=video_format)
    videoData.export(output_path, format="mp3")
    
    video.audioData = (open(output_path, "rb").read().hex())


# plays audio
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
