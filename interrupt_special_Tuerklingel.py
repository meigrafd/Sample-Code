#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# http://www.forum-raspberrypi.de/Thread-python-funktion-die-auf-bestimmte-eingabe-wartet
#
from __future__ import print_function
from Queue import Queue
from time import time, sleep
from RPi import GPIO
from functools import partial

#------------------------------------------------------------------------

# ISR
def interrupt_Event(q, channel):
    q.put( (channel, GPIO.input(channel)) )


def main():
    # GPIO pin
    taster = 17
    led = 27
    bell = 22
    gate = 23

    # special function time (in sec)
    specialTime = 10
    specialTimeout = 5
    # after switch was 'specialTime' pressed how many triggers needed to open gate
    specialTriggers = 3

    # only one of following:
    PULL = GPIO.PUD_DOWN    #GPIO -> GND
    #PULL = GPIO.PUD_UP     #GPIO -> 3V3

    # to use RaspberryPi pin numbers
    GPIO.setmode(GPIO.BCM)

    try:
        GPIO.setup(taster, GPIO.IN, pull_up_down=PULL)
        GPIO.setup(led, GPIO.OUT)
        GPIO.setup(bell, GPIO.OUT)
        GPIO.setup(gate, GPIO.OUT)
        queue=Queue()
        triggerCount=dict()
        triggerCount.update({ taster: 0 })
        triggerTime=0
        specialWait=False
        GPIO.add_event_detect(taster, GPIO.BOTH, callback=partial(interrupt_Event, queue), bouncetime=150)
        
        while True:
            job = queue.get()
            pin = job[0]
            state = job[1]
            if state == GPIO.HIGH:
                triggerTime = time()
            elif state == GPIO.LOW:
                triggerTime = time() - triggerTime
                
                if specialWait:
                    if triggerTime >= specialTimeout:
                        print("special Timeout!")
                        GPIO.output(led, GPIO.LOW)
                        specialWait=False
                        continue
                    
                    count = triggerCount.get(pin)
                    triggerCount.update({ pin: (count+1) })
                    if triggerCount.get(pin) == specialTriggers:
                        print("Opening Gate! previously pin was triggered '{}' times.".format( triggerCount.get(pin) ))
                        GPIO.output(gate, GPIO.HIGH)
                        sleep(1)
                        GPIO.output(gate, GPIO.LOW)
                        GPIO.output(led, GPIO.LOW)
                        specialWait=False
                        triggerCount.update({ pin: 0 })
                        continue
                
                if not specialWait and triggerTime >= specialTime:
                    print("please verify specialTriggers..")
                    GPIO.output(led, GPIO.HIGH)
                    specialWait=True
                
                else: #normal action
                    GPIO.output(bell, GPIO.HIGH)
                    sleep(1)
                    GPIO.output(bell, GPIO.LOW)
        
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
        print("\nQuit\n")


if __name__ == "__main__":
    main()


#EOF