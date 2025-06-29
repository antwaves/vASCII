from video import Video
import time 
import keyboard

v = Video() 
v.color = True
v.size = 75
v.resizeToHeight = True

v.from_file("videos//taxes.mp4").load_frames()
v.start_video()

while True:
    if keyboard.is_pressed("q"):
        v.stop()   
        break

    if keyboard.is_pressed("space"):
        pressed = True    

        while pressed:
            pressed = keyboard.is_pressed("space")
            time.sleep(0.1)
        
        v.flip_pause()   

    if v.kill.is_set():
        break                                 

    time.sleep(.05)
     