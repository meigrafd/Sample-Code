#!/usr/bin/python
#
# http://www.forum-raspberrypi.de/Thread-python-pi-cam-mit-bewegungsmelder?pid=151440#pid151440
#
import picamera
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Bewegungsmelder
GPIO.setup(24, GPIO.OUT)    #LED

x=1

try:
	while(True):
		if (GPIO.input(27) == GPIO.HIGH):
			print 'ausgeloest: ' + str(x)
			x += 1
			cam = picamera.PiCamera()
			cam.led = False
			cam.resolution = (1920, 1080)
			cam.start_preview()
			# Camera warm-up time
			time.sleep(2)
			with cam:
				for i, filename in enumerate(cam.capture_continuous('{timestamp:%H:%M:%S_%d-%m-%y}_{counter:04d}.jpg')):
					print filename
					GPIO.output(24,GPIO.HIGH)
					time.sleep(0.1)
					GPIO.output(24,GPIO.LOW)
					if i == 5-1:
						break
				cam.stop_preview()
		time.sleep(0.5)
except Exception, error:
	print 'Error: ' + str(error)
except (KeyboardInterrupt, SystemExit):
	print ' Quit'
	GPIO.cleanup()