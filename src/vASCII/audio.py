from pathlib import PurePath

from pydub import AudioSegment


# takes the video and creates a new mp3 file
def loadAudio(video, raw_input_path: str, raw_output_path: str, video_format: str):
    input_path = PurePath(raw_input_path)
    output_path = PurePath(raw_output_path)

    videoData = AudioSegment.from_file(input_path, format=video_format)
    videoData.export(output_path, format="mp3")

    video.audioData = open(output_path, "rb").read().hex()


# plays audio
def playAudio(video):
    if not video.playback.active:
        video.playback.load_file(video.audioOutputPath)

    if video.playback.paused:
        video.playback.resume()
    else:
        video.playback.play()


# pause the audioooo
def pauseAudio(video):
    if not video.playback.active:
        video.playback.load_file(video.audioOutputPath)

    video.playback.pause()
