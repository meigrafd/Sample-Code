#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# http://www.forum-raspberrypi.de/Thread-python-taster-der-stoppuhr-startet-und-stoppt
#
from __future__ import print_function
from time import sleep
from datetime import datetime
from RPi import GPIO
from Queue import Queue
from functools import partial


# http://stackoverflow.com/a/14190143
def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds


def print_duration(start, end):
    duration = end - start
    hours, mins, secs = convert_timedelta(duration)
    h_suffix=''; m_suffix=''; s_suffix=''
    if hours == 0 or hours > 1:
        h_suffix = 'n'
    if mins == 0 or mins > 1:
        m_suffix = 'n'
    if secs == 0 or secs > 1:
        s_suffix = 'n'
    print('{:2} Stunde{:1}, {:2} Minute{:1}, {:2} Sekunde{:1}'.format(hours,h_suffix, mins,m_suffix, secs,s_suffix))


def interrupt_Event(q, channel):
    q.put((channel, GPIO.input(channel)))


def main(switch=18, green=8, red=7):
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(switch, GPIO.IN)
    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(red, GPIO.OUT)
    queue = Queue()
    GPIO.add_event_detect(switch, GPIO.BOTH, callback=partial(interrupt_Event, queue), bouncetime=150)
    
    running=True
    start=datetime.now()
    end=datetime.now()
    try:
        while running:
            sleep(0.1)
            if not queue.empty():
                pin, state = queue.get()
                if state == GPIO.LOW:
                    start = datetime.now()
                    GPIO.output(green, False)
                    GPIO.output(red, True)
                elif state == GPIO.HIGH:
                    print_duration(start, datetime.now())
                    GPIO.output(green, True)
                    GPIO.output(red, False)
    
    except (KeyboardInterrupt, SystemExit):
        running=False
        GPIO.cleanup()
        print("\nQuit\n")


if __name__ == "__main__":
    main()


#EOF