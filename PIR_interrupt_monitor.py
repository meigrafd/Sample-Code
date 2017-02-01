#!/usr/bin/python
import time
import signal
import RPi.GPIO as GPIO

PIR_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

LogFile = "/tmp/motion.log"



## write line to file..
def writeInLog(logfile, message):
    with open(logfile, 'a') as fileObject:
        fileObject.write(str(message) + '\n')

def interrupt_event(pin):
    zeit = time.strftime('%d.%m.%Y %H:%M:%S')
    if GPIO.input(PIR_PIN) == GPIO.HIGH:
        print '{} Rising edge detected on {}' . format(zeit, pin)
        writeInLog(LogFile, zeit+"  Monitor on!")
    else:
        print '{} Falling edge detected on {}' . format(zeit, pin)
        writeInLog(LogFile, zeit+"  Monitor off!")

def main():
    try:
        GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, callback=interrupt_event, bouncetime=100)
        #keep script running
        signal.pause()
    except KeyboardInterrupt: # does not work if it runs in background.
        print "\nQuit"

if __name__ == '__main__':
    main()
    GPIO.cleanup()
    print "Ende des Scripts"
