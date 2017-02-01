#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# http://www.forum-raspberrypi.de/Thread-python-taster-mit-mehreren-funktionen?pid=134513#pid134513
#
# v0.1 by meigrafd
#
# https://github.com/SoCo/SoCo
#
import sys
from time import sleep, time
import RPi.GPIO as GPIO
import signal
from soco import SoCo
#------------------------------------------------------------------------

HOST = '192.168.178.83'

#GPIO pins
Play = 11
Pause = 12
Lauter = 16
Leiser = 18
Next = 13
Prev = 15

#special function time (in sec) for Play pin to switch playlist
SpecialTime = 1

# only one of following:
PULL = GPIO.PUD_DOWN    #GPIO -> GND
#PULL = GPIO.PUD_UP        #GPIO -> 3V3

# to use RaspberryPi pin numbers
GPIO.setmode(GPIO.BOARD)

#------------------------------------------------------------------------

# set up GPIO input channels
GPIO.setup(Play, GPIO.IN, pull_up_down = PULL)
GPIO.setup(Pause, GPIO.IN, pull_up_down = PULL)
GPIO.setup(Lauter, GPIO.IN, pull_up_down = PULL)
GPIO.setup(Leiser, GPIO.IN, pull_up_down = PULL)
GPIO.setup(Next, GPIO.IN, pull_up_down = PULL)
GPIO.setup(Prev, GPIO.IN, pull_up_down = PULL)

#------------------------------------------------------------------------

globalVar['timeTrigger'] = {}

def Interrupt_event(pin):
    # only for debug:
    if GPIO.input(pin) == GPIO.HIGH:
        print "rising edge on %s" % pin
    elif GPIO.input(pin) == GPIO.LOW:
        print "falling edge on %s" % pin

    if pin == Play:
        if GPIO.input(Play) == GPIO.HIGH:
            globalVar['timeTrigger'] = time()
        elif GPIO.input(Play) == GPIO.LOW:
            globalVar['timeTrigger'] = time() - globalVar['timeTrigger']
            if globalVar['timeTrigger'] >= SpecialTime:
                #special function: play another playlist
                print "special play"
            else: #normal play
                print "normal play"
                client.volume = 10
                client.play()

    elif GPIO.input(Pause) == GPIO.HIGH:
        client.pause()

    elif GPIO.input(Lauter) == GPIO.HIGH:
        client.volume += 2

    elif GPIO.input(Leiser) == GPIO.HIGH:
        client.volume -=2

    elif GPIO.input(Next) == GPIO.HIGH:
        client.next()

    elif GPIO.input(Prev) == GPIO.HIGH:
        client.previous()

    else:
        print "ERROR! Unknown GPIO pin triggered: %s" % pin

#------------------------------------------------------------------------

try:
    GPIO.add_event_detect(Play, GPIO.BOTH, callback=Interrupt_event, bouncetime=100)
    GPIO.add_event_detect(Pause, GPIO.RISING, callback=Interrupt_event, bouncetime=150)
    GPIO.add_event_detect(Lauter, GPIO.RISING, callback=Interrupt_event, bouncetime=150)
    GPIO.add_event_detect(Leiser, GPIO.RISING, callback=Interrupt_event, bouncetime=150)
    GPIO.add_event_detect(Next, GPIO.RISING, callback=Interrupt_event, bouncetime=150)
    GPIO.add_event_detect(Prev, GPIO.RISING, callback=Interrupt_event, bouncetime=150)

    globalVar['timeTrigger'] = 0
    client = SoCo(HOST)

    #keep script running
    signal.pause()
except (KeyboardInterrupt, SystemExit):
    GPIO.cleanup()
    print "\nQuit\n"