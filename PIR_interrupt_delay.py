#!/usr/bin/python2
#
# http://www.forum-raspberrypi.de/Thread-python-bewegungsmelder-mit-nachlaufzeit
#
from __future__ import print_function
from time import sleep
from datetime import datetime
from RPi import GPIO
from Queue import Queue
from functools import partial


def interrupt_event(q, channel):
    q.put( (channel, GPIO.input(channel), datetime.now()) )


def main(PIR_PIN=23, ACTION_PIN=21, DELTA=15):
    action=False
    action_time=datetime.now()
    queue = Queue()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ACTION_PIN, GPIO.OUT)
    GPIO.output(ACTION_PIN, GPIO.HIGH)
    GPIO.setup(PIR_PIN, GPIO.IN)
    try:
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=partial(interrupt_event, queue), bouncetime=100)
        while True:
            sleep(0.01)
            if not queue.empty():
                pin, state, dt = queue.get()
                action = True
                action_time = dt
                GPIO.output(ACTION_PIN, GPIO.LOW)
            if action and (datetime.now() - action_time).seconds > DELTA:
                action = False
                GPIO.output(ACTION_PIN, GPIO.HIGH)
                
    
    except KeyboardInterrupt:
        print("Quit")

if __name__ == '__main__':
    main()
    GPIO.cleanup()

#EOF