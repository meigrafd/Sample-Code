#!/usr/bin/python2.7
#
# Copyright (C) 2016 by meigrafd (meiraspi@gmail.com) published under the MIT License
# v1.0
#
# display picamera stream on pygame. pygame picamera lowest streaming latency
#
# http://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
# https://www.snip2code.com/Snippet/979508/OpenCV-VideoCapture-running-on-PyGame-on
#

from __future__ import print_function
from datetime import datetime
from picamera.array import PiRGBArray
from threading import Thread
from pygame.locals import *
from time import sleep, strftime
from sys import exit, stdout
import numpy as np
import pygame
import picamera


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
            self.frame = np.rot90(frameBuf.array)
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


def update_stream_screen(videostream, screen, pos):
    frame = pygame.surfarray.make_surface(videostream.read())
    return screen.blit(frame, pos)


# draw button as object
class Button(object):
    def __init__(self, _font=None, fontsize=21, fontaa=True, fontbg=None, bold=False, text='', pos=(0, 0), callback=None, screen=None):
        if not _font:
            _font = 'freesansbold.ttf'
        try:
            self.font = pygame.font.Font(_font, fontsize)
        except:
            self.font = pygame.font.SysFont(_font, fontsize)
        self.font_antialias = fontaa
        self.font_background = fontbg
        if bold == True:
            self.font.set_bold(1)
        else:
            self.font.set_bold(0)
        self._callback = callback
        self.screen = screen
        self.text = text
        self.pos = pos
        self.default_color = (100, 100, 100) #gray
        self.hover_color = (255, 255, 255)   #white
        self.hovered = False
        self.set_rect()

    def draw(self):
        self.set_rend()
        return self.screen.blit(self.rend, self.rect)

    def get_color(self):
        if self.hovered:
            return self.hover_color
        else:
            return self.default_color

    def set_rend(self):
        self.rend = self.font.render(self.text, self.font_antialias, self.get_color(), self.font_background)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

    def action(self):
        if self._callback:
            return self._callback()


def main():
    global DEBUG

    DEBUG = True
    debugFPS = True
    buttonHover = True

    screen_FPS = 30
    screen_width  = 640
    screen_height = 480

    stream_screen_pos = (200, 10) # vertical, horizontal
    stream_resolution = (320, 240)
    stream_framerate = 15
    picamera_led = True

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
    gray    = (100, 100, 100)

    size = (screen_width, screen_height)
    screen_xmax = screen_width - 2
    screen_ymax = screen_height - 1

    try:
        pygame.init()
        window = pygame.display.set_mode(size)
        window.fill(black)
        pygame.display.set_caption('picamera stream on pygame')

        vs = PiVideoStream(resolution=stream_resolution, framerate=stream_framerate, led=picamera_led)

        buttons = [
                    Button(text='Start', callback=vs.start, _font='droidsans', fontsize=42, pos=(30, 0), screen=window),
                    Button(text='Stop', callback=vs.stop, _font='droidsans', fontsize=42, pos=(30, 60), screen=window),
                  ]

        for button in buttons:
            button.default_color = white
            button.hover_color = gray
            pygame.display.update(button.draw())

        clock = pygame.time.Clock()
        while True:
            clock.tick(screen_FPS)
            dirtyrects = []

            if vs.running == True:
                dirtyrects.append(update_stream_screen(vs, window, stream_screen_pos))

            for event in pygame.event.get():
                if event.type in (QUIT, KEYDOWN):
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            printD(button.text)
                            button.action()

            if buttonHover:
                for button in buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                        dirtyrects.append(button.draw())
                    else:
                        button.hovered = False
                        dirtyrects.append(button.draw())

            if dirtyrects:
                pygame.display.update(dirtyrects)

            if (debugFPS == True and vs.running == True) or debugFPS == 'always':
                print('SCREEN: %.3f fps' % clock.get_fps())

    except (KeyboardInterrupt, SystemExit):
        print('Quit')
        vs.quit()
        pygame.quit()
    except Exception, error:
        print('Error: ' + str(error))
        exit()


if __name__ == '__main__':
    main()
