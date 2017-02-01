#!/usr/bin/python
from __future__ import print_function
import RPi.GPIO as GPIO
import time
import pigpio

#------------------------------------------------------------------------
# use the raspi board pin number
#GPIO.setmode(GPIO.BOARD)
# use the gpio number
GPIO.setmode(GPIO.BCM)

# only one of following for GPIO.IN:
PULL = GPIO.PUD_DOWN  #GPIO -> GND
#PULL = GPIO.PUD_UP   #GPIO -> 3V3

Taster1 = 27

slaveHost = '192.168.0.101'
slavePort = 8888
slaveGPIO = 25
#------------------------------------------------------------------------

def interrupt_event(pin):
    if GPIO.input(pin) == GPIO.HIGH:
        slave.write(slaveGPIO, 1)
    else:
        slave.write(slaveGPIO, 0)

def main():
    GPIO.setup(Taster1, GPIO.IN, pull_up_down=PULL)
    slave = pigpio.pi(slaveHost, slavePort)
    slave.set_mode(slaveGPIO, pigpio.OUTPUT)
    GPIO.add_event_detect(Taster1, GPIO.BOTH, callback=interrupt_event)
    #keep script running
    while True:
        time.sleep(0.5)

if __name__ == '__main__': 
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("\nQuit\n")
        GPIO.cleanup()
        slave.stop()