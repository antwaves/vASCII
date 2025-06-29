import os
import cv2
import time
from threading import Thread, Event

import just_playback
from pathlib import PurePath

import videoProcess
import videoExport
import helper
import audio


class VideoError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message


class Video:
    def __init__(self):
        #internal data/handles
        self.videoCap = None
        self.audioData = None
        self.playback = just_playback.Playback()

        self.frames = []
        self.frameDiffs = []
        self.fps = None

        self.paused = Event()
        self.kill = Event()
        self.printThread = None

        #compression preferences
        self.size = 50
        self.resizeToHeight = False

        self.skip = None
        self.fpsLimit = 12
        self.frameTime = None
        self.frameCount = None

        self.colorReduction = 16

        #other preferences
        self.mute = False
        self.audioOutputPath = "output.mp3"

        self.color = False
        

    def from_file(self, raw_path: str):
        path = PurePath(raw_path)
        self.videoCap = cv2.VideoCapture(PurePath(path))

        if self.videoCap.isOpened():
            self.frameCount = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.videoCap.get(cv2.CAP_PROP_FPS)

            if self.fpsLimit:
                self.skip = self.fps // self.fpsLimit  
                self.fps = int(self.fps // self.skip)
                self.frameCount = int(self.frameCount // self.skip)
                self.frameTime = 1 / self.fps
            
            video_ext = os.path.splitext(str(path))[1][1:]
            audio.loadAudio(self, path, self.audioOutputPath, video_ext)
        else:
            raise VideoError(f"FileExistsError: Does '{path}' really exist")
        
        return self


    def load_frames(self, logger = None):
        if self.videoCap:
            videoProcess.processVideo(self, logger)
        else:
            raise VideoError("VideoMissingError: Video is missing. Call a video loading function before loading frames")

        return self


    def from_import(self, path: str, logger = None) -> None:
        videoExport.decodeVideo(path, self, logger)
    

    def export_video(self, path: str = "output.txt", logger = None) -> None:
        if self.videoCap:
            videoExport.encodeVideo(path, self, logger)
        else:
            raise VideoError("VideoMissingError: Video is missing. Call a video loading function before exporting frames")


    def print_video(self) -> None:
        if not self.frameDiffs:
            raise VideoError("FramesMissingError: Frames are missing. Call a frame loading function before printing frames")
        print("\33[?25l") #hide mouse


        # see https://stackoverflow.com/questions/67329314/creating-a-precise-time-interval-with-no-drift-over-long-periods-of-time
        begin = time.time()   
        pauseCount = 0 
        targetTime = 0

        for i in range(len(self.frameDiffs)):
            if self.paused.is_set():
                while self.paused.is_set():
                    time.sleep(0.05)
            
            if self.kill.is_set():
                break

            print("\033[H" + self.frameDiffs[i])

            # check if the current time is behind the current expected time, and sleep if so
            target = (begin + targetTime)
            sleepTime = target - time.time()
            if sleepTime > 0:
                time.sleep(sleepTime)
            
            targetTime += self.frameTime    
    

    def start_video(self) -> None:
        self.kill.clear()
        t = Thread(target=self.print_video, args=())
        t.start()
        self.printThread = t
    

    def pause(self) -> None:
        if self.printThread:
            self.paused.set()
    

    def unpause(self) -> None:
        if self.printThread:
            self.paused.clear()
    

    def stop(self) -> None:
        if self.printThread:
            self.kill.set()


v = Video()

v.from_file("videos//taxes.mp4").load_frames()
v.export_video()

#v.start_video()