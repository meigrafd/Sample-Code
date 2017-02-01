#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import signal

RPv = GPIO.RPI_REVISION
if RPv == 1:
	GPIOpins = [0,1,4,17,21,22,10,9,11,18,23,24,25,8,7]
elif RPv == 2 or RPv == 3:
	GPIOpins = [2,3,4,17,27,22,10,9,11,18,23,24,25,8,7]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for gpin in GPIOpins:
	GPIO.setup(gpin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #GPIO -> GND
#	GPIO.setup(gpin, GPIO.IN, pull_up_down = GPIO.PUD_UP) #GPIO -> 3V3

def Interrupt_event(pin):
	Zeit = time.asctime()
	print("{} -> GPIO {} ausgeloest!".format(Zeit, pin))

try:
	for gpin in GPIOpins:
		GPIO.add_event_detect(gpin, GPIO.RISING, callback=Interrupt_event, bouncetime=100)
	#keep script running
	signal.pause()
except KeyboardInterrupt:
	print("\nQuit\n")

GPIO.cleanup()