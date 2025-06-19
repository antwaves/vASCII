import cv2
import time
import threading
import just_playback

import videoProcess
import helper
import audio


class VideoError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message


class Video:
    def __init__(self):
        #create defaults
        self.cap = None

        self.mute = False
        self.audio = just_playback.Playback() if not self.mute else None

        self.size = 100
        self.resizeToHeight = False

        self.skip = None
        self.fps = None
        self.fpsLimit = 12
        self.frameTime = None
        self.frameCount = None

        self.color = True
        self.colorReduction = 16

        self.frames = []
        self.frameDiffs = []

        self.paused = False
        self.pauseTime = 0

        self.videoPath = None


    def from_file(self, path: str) -> None:
        self.videoPath = path
        self.cap = cv2.VideoCapture(path)

        if self.cap.isOpened():
            self.frameCount = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)

            if self.fpsLimit:
                self.skip = self.fps // self.fpsLimit  
                self.fps //= self.skip
                self.frameCount = int(self.frameCount // self.skip)
                self.frameTime = 1 / self.fps
        else:
            raise VideoError(f"FileExistsError: Does '{path}' really exist")


    def load_frames(self, logger = None) -> None:
        # if not self.mute:
        #     #FIX ME!
        #     t1 = threading.Thread(target=self.audio.loadAudio, args=(self.videoPath,))
        #     t1.start() 
        
        if self.cap:
            videoProcess.processVideo(self, logger)
        else:
            raise VideoError("VideoMissingError: Call a video loading function before loading frames")
        
        # if not self.mute:
        #     t1.join()
    

    def import_frames(self, logger = None) -> None:
        pass

    def play_video(self) -> None:
        print("\33[?25l")

        #if not config.mute:
            #audio.playAudio(playback)  # start audio

        # see https://stackoverflow.com/questions/67329314/creating-a-precise-time-interval-with-no-drift-over-long-periods-of-time
        begin = time.time()
        if not self.frameDiffs:
            raise VideoError("FramesMissingError: Call a frame loading function before printing frames")
        
        targetTime = 0
        for i in range(len(self.frameDiffs)):
            print(self.frameDiffs[i])

            # check if the current time is behind the current expected time, and sleep if so
            target = (begin + targetTime)
            sleepTime = target - time.time()
            if sleepTime > 0:
                time.sleep(sleepTime)
            
            targetTime += self.frameTime


v = Video()
v.from_file("videos/taxes.mp4")
#v.load_frames(helper.log)
print("ready?")
v.play_video()
