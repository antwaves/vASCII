from pathlib import PurePath
from io import BytesIO

from pydub import AudioSegment


# takes the video and creates a new mp3 file
def loadAudio(video, raw_input_path: str, raw_output_path: str, video_format: str) -> None:
    input_path = PurePath(raw_input_path)
    output_path = PurePath(raw_output_path)

    try:
        videoData = AudioSegment.from_file(input_path, format=video_format)
        videoData.export(output_path, format="mp3")
        video.audioData = open(output_path, "rb").read().hex()
    except IndexError: #lack of audioc
        pass
    except Exception as e:
        print(f"Unintended exception '{e}' was thrown in loadAudio")


def loadFromHex(hex: str, output: str) -> None:
    audio = AudioSegment.from_file(BytesIO(bytes.fromhex(hex)), "mp3")
    audio.export(output, format="mp3")


# plays audio
def playAudio(video) -> None:
    if video.audioData:
        if not video.playback.active:
            video.playback.load_file(video.audioOutputPath)

        if video.playback.paused:
            video.playback.resume()
        else:
            video.playback.play()


# pause the audioooo
def pauseAudio(video) -> None:
    if video.audioData:
        if not video.playback.active:
            video.playback.load_file(video.audioOutputPath)
        video.playback.pause()
