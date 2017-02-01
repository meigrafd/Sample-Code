#!/usr/bin/python2.7
#
# Copyright (C) 2016 by meigrafd (meiraspi@gmail.com) published under the MIT License
# v1.0
#
# display picamera stream on Tkinter. lowest streaming latency
#

from __future__ import print_function
from datetime import datetime
from picamera.array import PiRGBArray
from PIL import Image, ImageTk
from threading import Thread
from time import sleep, strftime
from sys import exit, stdout
import picamera
import Tkinter as tkinter
import numpy as np


def printD(message):
    if DEBUG:
        print('[{}]  {}'.format(strftime('%H:%M:%S'), message))
        stdout.flush()


class PiVideoStream(object):
    def __init__(self, resolution=(320, 240), format='rgb', framerate=30, led=True):
        self.camera_led = led
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True)
        self.frame = None
        self.running = False
        #dirty but currently the only way so it works immediately
        self.start()
        self.stop()

    def start(self):
        # start the thread to read frames from the video stream
        if self.camera_led:
            self.camera.led = self.camera_led
        self.running = True
        Thread(target=self.update, args=()).start()
        sleep(0.2) #give videostream some time to start befor frames can be read

    def update(self):
        # keep looping infinitely until the thread is stopped
        for frameBuf in self.stream:
            # grab the frame from the stream and clear the stream in preparation for the next frame
            self.frame = frameBuf.array
            self.rawCapture.truncate(0)
            # if the thread indicator variable is set, stop the thread
            if self.running == False:
                self.camera.led = False
                return

    def quit(self):
        # resource camera resources
        try:
            self.running = False
            self.stream.close()
            self.rawCapture.close()
            self.camera.close()
        except:
            pass

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.running = False


class GUI(object):
    def __init__(self, videostream, resolution="640x480", stream_resolution=(320, 240)):
        self.videostream = videostream
        self.resolution = resolution
        self.stream_resolution = stream_resolution
        self.running = False
        self.master = tkinter.Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.main()
        self.master.mainloop()

    def main(self):
        self.master.geometry(self.resolution)
        self.master.title("picamera stream on tkinter")
        self.startstop_button = tkinter.Button(master=self.master, text="Start", bg="green", command=self.startstop_stream)
        self.startstop_button.place(x=10, y=10, height=50, width=50)
        self.stream_label = tkinter.Label(master=self.master)
        self.stream_label.place(x=60, y=10)
        self.exit_button = tkinter.Button(master=self.master, bg="#229", fg="white", text="Exit", command=self.quit)
        self.exit_button.place(x=10, y=200, height=50, width=50)

    def startstop_stream(self):
        # start
        if self.running == False:
            printD("Start")
            self.startstop_button.config(bg="red", text="Stop")
            self.running = True
            self.videostream.start()
            self.update_stream()
        # stop
        else:
            printD("Stop")
            self.startstop_button.config(bg="green", text="Start")
            self.running = False
            self.videostream.stop()

    def update_stream(self):
        frame = self.videostream.read()
        image = ImageTk.PhotoImage(Image.fromarray(frame))
        self.stream_label.configure(image=image)
        self.stream_label.image = image
        if self.running == True:
            self.master.after(70, self.update_stream)

    def quit(self):
        self.running = False
        self.videostream.quit()
        self.master.destroy()
        print('Quit')


def main():
    global DEBUG

    DEBUG = True

    screen_width  = 400
    screen_height = 300

    stream_resolution = (320, 240)
    stream_framerate = 15
    picamera_led = True

    try:

        vs = PiVideoStream(resolution=stream_resolution, framerate=stream_framerate, led=picamera_led)
        tkinter_app = GUI(videostream=vs, resolution="{0}x{1}".format(screen_width, screen_height), stream_resolution=stream_resolution)

    except (KeyboardInterrupt, SystemExit):
        print('Quit')
        tkinter_app.quit()
    except Exception, error:
        print('Error: ' + str(error))
        exit()


if __name__ == '__main__':
    main()