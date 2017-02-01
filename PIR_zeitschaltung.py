#!/usr/bin/python

import RPi.GPIO as GPIO
import signal, time

#---------------------------------------------------------------------

#GPIO pins
PIR = 7
REL = 6

#Times in 24h Format
startTime = 23
endTime = 06

#---------------------------------------------------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(REL, GPIO.OUT)

def relais():
	GPIO.output(REL, GPIO.HIGH)
	time.sleep(100)
	GPIO.output(REL, GPIO.LOW)
	print "Done"

def interrupt_event(pin):
	hourNow = time.strftime('%H')
	startTime2 = startTime - 1
	if startTime2 == -1:
		startTime2 = 23
	if (hourNow > startTime2) and (hourNow is not endTime):
		print "Motion detected"
		relais()

def main():
	try:
		GPIO.add_event_detect(PIR, GPIO.RISING, callback=interrupt_event, bouncetime=100)
		#keep script running
		signal.pause()
	except (KeyboardInterrupt, SystemExit):
		print "Quit"

if __name__ == '__main__':
	main()
	GPIO.cleanup()
	print "End of Script"