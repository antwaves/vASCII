import threading
import keyboard
import time

import just_playback
import cv2

import videoProcess
import videoExport
import userInput
import config
import audio

frames = []
frameDiffs = []

paused = False
pauseTime = 0

info = userInput.grabInput() #get the config input
if info: #do frame calcs if importing
    frameDiffs = info[0]
    frameTime = 1 / int(float(info[1][2])) 

path = config.videosFolder + "\\" + config.videoStr + "." + config.videoExt
begin = time.time()  # remove if needed
cap = cv2.VideoCapture(path)  # cap is the video object

if cap.isOpened():
    print("\33[?25l")  # hide cursor

    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    #calc frame stuff
    if config.fpsLimit and not config.importing:
        skip = fps // config.fpsLimit  
        fps //= skip
        frameCount //= skip
        frameTime = 1 / fps
    
    playback = just_playback.Playback()  # init audio object
    if not config.mute:
        t1 = threading.Thread(target=audio.loadAudio, args=(path,))
        t1.start()  # start a thread that grabs the audio in the background

    if not config.importing: #dont do the thing if importing
        videoProcess.processVideo(cap, frames, frameDiffs, frameCount)  # process the video into text
        
    if not config.mute:
        t1.join()  # join the audio thread back to pain
    
    if config.exporting:  #export the video if exporting
        videoExport.encodeVideo(frameDiffs, config.videoStr, fps, config.color)

    print("\nZOOM OUT!!!!! (and then press enter)")
    print(f"Job completed in {time.time() - begin} total seconds")
    keyboard.wait("enter")

    # start audio
    if not config.mute:
        audio.playAudio(playback)  # start audio

    # see https://stackoverflow.com/questions/67329314/creating-a-precise-time-interval-with-no-drift-over-long-periods-of-time
    begin = time.time()
    for i in range(len(frameDiffs)):
        if not paused:
            print(frameDiffs[i])

            # check if the current time is behind the current expected time, and sleep if so
            target = (begin + i * frameTime) + pauseTime
            sleepTime = target - time.time()
            if sleepTime > 0:
                time.sleep(sleepTime)

            # check if pausing
            if keyboard.is_pressed("space"):
                t = time.time()  # start measuring time
                pressed = True
                paused = True

                while pressed:  # wait for user to let go of space
                    pressed = keyboard.is_pressed("space")
                    time.sleep(0.1)

                if not config.mute:  # pause audio
                    audio.pauseAudio(playback)

                pauseTime += time.time() - t  # add offset

        else:
            t = time.time()

            # check if unpausing. block thread until unpaused
            keyboard.wait("space")
            if keyboard.is_pressed("space"):
                pressed = True
                paused = False

                while pressed:  # wait for user to let for of space
                    pressed = keyboard.is_pressed("space")
                    time.sleep(0.1)

                if not config.mute:  # unpause audio
                    audio.playAudio(playback)

            pauseTime += time.time() - t  # add offset
else:
    print(f"Video failed to open")
