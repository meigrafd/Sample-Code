#!/usr/bin/python2
#
# optimized version 2
#
from __future__ import print_function
from time import sleep
from datetime import datetime, strftime
from RPi import GPIO
from Queue import Queue
from functools import partial


def interrupt_event(q, channel):
    q.put( (channel, GPIO.input(channel), datetime.now()) )


def main(PIR_PIN=24):
    queue = Queue()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)
    try:
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=partial(interrupt_event, queue), bouncetime=100)
        while True:
            sleep(0.01)
            if not queue.empty():
                pin, state, dt = queue.get()
                print('[{}] Motion detected'.format( dt.strftime('%d.%m.%Y %H:%M:%S') )
                # hier kann man dann zB. mit dem picamera modul ein Bild schiessen ...
    
    except KeyboardInterrupt: # does not work if it runs in background.
        print("Quit")

if __name__ == '__main__':
    main()
    GPIO.cleanup()
    print("Ende des Scripts")

#EOF