#!/usr/bin/python
#
# (c) by meigrafd
#
# records for 20sec after motion detected and resets timer after new motion while record.
#
from __future__ import absolute_import, division, print_function
import time
from RPi import GPIO

PIR_pin=17

record_to_file = '/tmp/video.h264'

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_pin, GPIO.IN)
dictionary = {}
dictionary['motion'] = False
dictionary['counter'] = 0


def interrupt_event(channel):
    dictionary['motion'] = True

if __name__ == '__main__':
    try:
        print('Programmstart')
        GPIO.add_event_detect(PIR_pin, GPIO.RISING, callback=interrupt_event, bouncetime=100)
        
        with picamera.PiCamera() as camera:
            camera.resolution = (800,600)
            camera.framerate = 24
            while True:
                if dictionary['motion'] == True:
                    dictionary['motion'] = False
                    if dictionary['counter'] == 0:
                        print('Beginn der Videoaufzeichnung')
                        camera.start_preview()
                        time.sleep(2)
                        camera.start_recording(record_to_file, format='h264', quality=30)
                    dictionary['counter'] = 21
                if dictionary['counter'] > 0:
                    dictionary['counter'] -= 1
                if dictionary['counter'] == 1:
                    print('Ende der Videoaufzeichnung')
                    camera.stop_recording()
                time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
