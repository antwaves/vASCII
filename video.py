import cv2
import threading
import just_playback

import videoProcess
import audio

class Video:
    def __init__(self):
        #create defaults
        self.cap = None

        self.mute = False
        self.audio = just_playback.Playback() if not mute else None

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
            self.frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = cap.get(cv2.CAP_PROP_FPS)

            if self.fpsLimit:
                self.skip = self.fps // self.fpsLimit  
                self.fps //= self.skip
                self.frameCount //= self.skip
                self.frameTime = 1 / self.fps
        else:
            raise FileExistsError 


    def load_frames(self, cap: cv2.VideoCapture, logger: Function = None) -> None:
        if not self.mute:
            #FIX ME!
            t1 = threading.Thread(target=self.audio.loadAudio, args=(self.videoPath,))
            t1.start() 
        
        if self.cap:
            videoProcess.processVideo(self.cap, self.frames, self.frameDiffs, self.frameCount)
        
        if not self.mute:
            t1.join()
    

    def play_video(self):
        pass


v = Video()
v.from_file("")
            

