#!/usr/bin/python
#
# v0.5 by meigrafd
# http://www.forum-raspberrypi.de/Thread-python-python-script-gpio-event-pushbullet-notification-picam?pid=146167#pid146167
#
import time, signal, os, glob
import RPi.GPIO as GPIO
import picamera
from pushbullet import Pushbullet
from datetime import datetime
import urllib3

#---------------------------------------------------------------------
PIR_PIN = 24
API_KEY = 'boXXlYbzxigg0SU5cbvnNe8aqiQuW9pb'

# only one of following:
PULL = GPIO.PUD_DOWN    #GPIO -> GND
#PULL = GPIO.PUD_UP        #GPIO -> 3V3
#---------------------------------------------------------------------

def send_push(file):
	try:
		urllib3.disable_warnings()
		pb = Pushbullet(API_KEY)
		#push = pb.push_note(pb.devices[3]['iden'],'Alarm', 'Motion detected')
		push = pb.push_note('Alarm', 'Motion detected')
		print "push-uploading file.."
		with open(file, 'rb') as vid:
			file_data = pb.upload_file(vid, 'video.mkv')
		push = pb.push_file(**file_data)
		# only for debug:
		#pushes = pb.get_pushes()
		#latest = pushes[0]
		#print latest
	except Exception, error:
		print "Error in send_push: " + str(error)

def picam_record( ToFile='/tmp/video.mkv', Resolution=(1024,768), Format='h264', Recordtime=10, Quality=30, Framerate=24, Led=False ):
	timestamp = time.time()
	t = datetime.fromtimestamp(timestamp)
	try:
		with picamera.PiCamera() as camera:
			print 'Starting record to %s' % ToFile
			camera.led = Led
			camera.resolution = Resolution
			camera.framerate = Framerate
			camera.start_preview()
			camera.annotate_text = t.strftime('%d.%m.%Y %H:%M:%S')
			camera.start_recording(ToFile, format=Format, quality=Quality)
			camera.wait_recording(Recordtime)
			print 'Captured %s' % ToFile
			camera.stop_recording()
			camera.stop_preview()
		# send push message and file
		send_push(ToFile)
		# rename file
		#get dirname and filename without extension
		dirName = os.path.dirname(ToFile)
		fileName = os.path.basename(ToFile)
		fileBasename = os.path.splitext(fileName)[0]
		fileExtension = os.path.splitext(fileName)[1]
		#rename file with timestamp
		newFile = dirName + '/' + fileBasename + '_' + t.strftime('%d%m%Y_%H%M%S') + fileExtension
		os.rename(ToFile, newFile)
		print 'Renamed file to %s' % newFile
	except Exception, error:
		print "Error in picam_record: " + str(error)

def interrupt_event(pin):
	zeit = time.strftime('%d.%m.%Y %H:%M:%S')
	print '{} -> GPIO {} ausgeloest! Motion detected'.format(zeit, pin)
	#picam_record()
	picam_record(ToFile='/media/usbstick/cam/video.h264', Recordtime=20, Quality=20)


if __name__ == '__main__':
	try:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down = PULL)
		GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=interrupt_event, bouncetime=100)
		#keep script running
		signal.pause()
	except (KeyboardInterrupt, SystemExit):
		print 'Quit'
		GPIO.cleanup()