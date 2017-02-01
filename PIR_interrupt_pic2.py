#!/usr/bin/python
# coding: utf-8
#
# http://www.forum-raspberrypi.de/Thread-bild-per-raspistill-in-python?pid=146362#pid146362
#
import time, picamera, RPi.GPIO as GPIO, signal
#------------------------------------------------------------------------
PIR_PIN = 17

# to use RaspberryPi gpio# (BCM) or pin# (BOARD)
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)

# only one of following:
PULL = GPIO.PUD_DOWN    #GPIO -> GND
#PULL = GPIO.PUD_UP        #GPIO -> 3V3
#------------------------------------------------------------------------

GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=PULL)

def picam_pic( ToPath='/tmp/', Resolution=(1024,768), Format='jpeg', Quality=100, Led=False ):
	try:
		with picamera.PiCamera() as camera:
			camera.led = Led
			camera.resolution = Resolution
			camera.start_preview()
			# Camera warm-up time
			time.sleep(2)
			if Format == 'jpeg':
				for filename in camera.capture_continuous(ToPath + '{timestamp:%d.%m_%H-%M-%S}Uhr.jpg', format=Format, quality=Quality):
					print 'Captured %s' % filename
					break
			else:
				for filename in camera.capture_continuous(ToPath + '{timestamp:%d.%m_%H-%M-%S}Uhr.' + str(Format), format=Format):
					print 'Captured %s' % filename
					break
			camera.stop_preview()
	except Exception, error:
		print 'Error in picam_pic: ' + str(error)

def interrupt_event(pin):
	zeit = time.strftime('%d.%m.%Y %H:%M:%S')
	print '{} -> GPIO {} ausgeloest!'.format(zeit, pin)
	#picam_pic()
	picam_pic(ToPath='/home/pi/bilder/', Led=True)

try:
	GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=interrupt_event, bouncetime=100)
	#keep script running
	signal.pause()
except (KeyboardInterrupt, SystemExit):
	print ' Quit '
	GPIO.cleanup()