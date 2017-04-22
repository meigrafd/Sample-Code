#!/usr/bin/python3
#
# http://www.forum-raspberrypi.de/Thread-python-gpiozero-und-motion-sensor
#
from __future__ import print_function
from gpiozero import MotionSensor
import signal
from itertools import count


def counting(counter):
    print(next(counter))


def main():
    try:
        counter = count(1)
        with MotionSensor(11) as pir:
            pir.when_motion = lambda: counting(counter)
            signal.pause()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()