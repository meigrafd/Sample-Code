#!/usr/bin/python2
#
# http://www.forum-raspberrypi.de/Thread-python-script-mit-einer-taste-starten-und-stoppen?pid=272277#pid272277
#

from __future__ import print_function
from gpiozero import Button
import signal
import datetime


def count_time(button):
    while button.is_held:
        if button.held_time:
            time_during_pushed = datetime.timedelta(seconds=button.held_time)
            print(time_during_pushed)
    compare_time(time_during_pushed)


def compare_time(time_during_pushed):
    print(time_during_pushed)
    if time_during_pushed <= datetime.timedelta(seconds=4):
        print("start_something()")
    else:
        print("stop_somthing()")


def main():
    try:
        with Button(21, hold_time=0) as button:
            button.when_held = lambda: count_time(button)
            signal.pause()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()