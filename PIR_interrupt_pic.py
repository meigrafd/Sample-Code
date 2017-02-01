#!/usr/bin/python3
# coding=utf-8
#
# http://www.forum-raspberrypi.de/Thread-bild-per-raspistill-in-python?pid=146362#pid146362
#
import time, picamera, RPi.GPIO as GPIO

PIR_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def motion(pin):
	print("Bewegung erkannt")
	with picamera.PiCamera() as camera:
		for filename in camera.capture_continuous('/home/pi/Desktop/Fotos/{timestamp:%d.%m_%H-%M-%S}Uhr.jpg'):
			print('Captured %s' % filename)
			break

try:
	GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion)
	while True:
		time.sleep(0.5)
except (KeyboardInterrupt, SystemExit):
	GPIO.cleanup()