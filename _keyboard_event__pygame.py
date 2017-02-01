#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO

#------------------------------------------------------------------------

red = 17
green = 22

# to use RaspberryPi gpio# (BCM) or pin# (BOARD)
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

#------------------------------------------------------------------------

GPIO.setwarnings(False)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

os.environ["SDL_FBDEV"] = "/dev/fb1"
width  = 320
height = 240
size = (width, height)
pygame.display.init()
screen = pygame.display.set_mode(size)

def schalten(pin):
    current_state = GPIO.input(pin)
    GPIO.output(pin, not current_state)
    print('switched GPIOpin {} from {} to {}' . format(pin, current_state, (not current_state)))


try:
    running=True
    clock = pygame.time.Clock()
    # run the game loop
    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                #https://www.pygame.org/docs/ref/key.html
                if event.key == K_a:
                    print('Key "a" is pressed')
                    schalten(red)
                elif event.key == K_1:
                    print('Key "1" is pressed')
                    schalten(green)
                else:
                    print('Unknown Key: "{}"'.format(str(pygame.key.name(event.key))))

except pygame.error, perr:
    print('pygame Error: ' + str(perr))
except (KeyboardInterrupt, SystemExit):
    running = False
    GPIO.cleanup()
    print('\nQuit\n')