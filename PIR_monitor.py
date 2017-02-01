#!/usr/bin/env python
import sys
from time import time, sleep
from subprocess import call
from RPi import GPIO

PIR_PIN = 23
SHUTOFF_DELAY = 60 

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)
    turned_off = False
    last_motion_time = time()

    while True:
        if GPIO.input(PIR_PIN):
            last_motion_time = time()
            print ".",
            sys.stdout.flush()
            if turned_off:
                turned_off = False
                turn_on()
        else:
            if not turned_off and time() > (last_motion_time + SHUTOFF_DELAY):
                turned_off = True
                turn_off()
        sleep(0.01)

def turn_on():
    call("vcgencmd display_power 1", shell=True)

def turn_off():
    call("vcgencmd display_power 0", shell=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()