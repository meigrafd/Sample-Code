#!/usr/bin/python2.7
#
# Copyright (C) 2016 by meiraspi@gmail.com published under the MIT License
#
# display pygame window from picamera
#
# http://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
# https://www.snip2code.com/Snippet/979508/OpenCV-VideoCapture-running-on-PyGame-on
#

from datetime import datetime
from picamera.array import PiRGBArray
from threading import Thread
from pygame.locals import *
from time import sleep
from sys import exit
import numpy as np
import pygame
import picamera


class PiVideoStream:
    def __init__(self, resolution=(320, 240), format='rgb', framerate=32, led=True):
        # initialize the camera and stream
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True)
        # initialize the frame and the variable used to indicate if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        self.camera.led = led
        return self
 
    def update(self):
        # keep looping infinitely until the thread is stopped
        for frameBuf in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = np.rot90(frameBuf.array)
            self.rawCapture.truncate(0)
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.camera.led = False
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame
 
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


def update_stream_screen(videostream, screen):
    dirtyrects = []
    frame = pygame.surfarray.make_surface(videostream.read())
    #dirtyrects.append( screen.fill(black) )
    dirtyrects.append( screen.blit(frame, (30,30)) )
    pygame.display.update(dirtyrects)



if __name__ == '__main__':
    width  = 640
    height = 480

    # colors    R    G    B
    white   = (255, 255, 255)
    red     = (255,   0,   0)
    green   = (  0, 255,   0)
    blue    = (  0,   0, 255)
    black   = (  0,   0,   0)
    cyan    = ( 50, 255, 255)
    magenta = (255,   0, 255)
    yellow  = (255, 255,   0)
    orange  = (255, 127,   0)

    size = (width, height)
    xmax = width - 2
    ymax = height - 1

    try:
        pygame.init()
        window = pygame.display.set_mode(size)
        window.fill(black)
        pygame.display.set_caption("picamera stream on pygame")
        clock = pygame.time.Clock()
        vs = PiVideoStream().start()
        sleep(0.2)
        
        while True:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type in (QUIT, KEYDOWN):
                    exit()
                    
            update_stream_screen(vs, window)
            print 'FRAMERATE: %.3f fps' % clock.get_fps()

    except (KeyboardInterrupt, SystemExit):
        print 'Quit'
        vs.stop()
        pygame.quit()
    except Exception, error:
        print "Error: " + str(error)
        exit()
