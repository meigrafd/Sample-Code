#!/usr/bin/python
#
# http://www.forum-raspberrypi.de/Thread-python-interrupt-loest-ungewuenscht-aus?pid=123729#pid123729
# http://www.forum-raspberrypi.de/Thread-python-python-hilfe-bei-python-script-fuer-drehzahlmesser-mit-ir-lichtschranke?pid=119477#pid119477
# http://www.forum-raspberrypi.de/Thread-python-auf-flanken-reagieren-und-mehrer-befehle-ausfuehren?pid=123621#pid123621
#
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import signal

gpioPin1 = 4
gpioPin2 = 7
gpioPin3 = 11
gpioPin4 = 12

# only one of following:
PULL = GPIO.PUD_DOWN    #GPIO -> GND
#PULL = GPIO.PUD_UP        #GPIO -> 3V3

# to use RaspberryPi gpio# (BCM) or pin# (BOARD)
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)
GPIO.setup(gpioPin1, GPIO.IN, pull_up_down = PULL)
GPIO.setup(gpioPin2, GPIO.IN, pull_up_down = PULL)
GPIO.setup(gpioPin3, GPIO.IN, pull_up_down = PULL)
GPIO.setup(gpioPin4, GPIO.IN, pull_up_down = PULL)

def Interrupt_event(pin):
	if GPIO.input(pin): # if gpioPin == 1
		print "Rising edge detected on %s" % pin
	else:
		print "Falling edge detected on %s" % pin


try:
	GPIO.add_event_detect(gpioPin1, GPIO.BOTH, callback=Interrupt_event, bouncetime=150)
	GPIO.add_event_detect(gpioPin2, GPIO.BOTH, callback=Interrupt_event, bouncetime=150)
	GPIO.add_event_detect(gpioPin3, GPIO.BOTH, callback=Interrupt_event, bouncetime=150)
	GPIO.add_event_detect(gpioPin4, GPIO.BOTH, callback=Interrupt_event, bouncetime=150)

	#keep script running
	signal.pause()

except KeyboardInterrupt:
	print "\nQuit\n"

GPIO.cleanup()