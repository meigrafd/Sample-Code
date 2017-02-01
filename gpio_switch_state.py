#!/usr/bin/python
#
# switch GPIO state -  by meigrafd
#
import time, RPi.GPIO as GPIO

PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

def switch_state():
	while True:
		# get current state
		current_state = GPIO.input(PIN)
		# switch state
		GPIO.output(PIN, not current_state)
		print 'switched GPIOpin {} from {} to {}' . format(PIN, current_state, (not current_state))
		time.sleep(1)

try:
	switch_state()
except (KeyboardInterrupt, SystemExit):
	print 'Quit'
	GPIO.cleanup()
