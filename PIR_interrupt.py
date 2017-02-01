#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import signal

PIR_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

def interrupt_event(pin):
    zeit = time.strftime('%d.%m.%Y %H:%M:%S')
    print '{} -> GPIO {} ausgeloest! Motion detected'.format(zeit, pin)
    # hier kann man dann z.B. mit dem picamera modul ein Bild schiessen ... 

def main():
    try:
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=interrupt_event, bouncetime=100)
        #keep script running
        signal.pause()
    except KeyboardInterrupt: # does not work if it runs in background.
        print "Quit"

if __name__ == '__main__':
    main()
    GPIO.cleanup()
    print "Ende des Scripts"
