import RPi.GPIO as GPIO
import threading
import signal

#------------------------------------------------------------------------

#GPIO pins
tasterRauf = 5
tasterRunter = 6
rolloRauf = 17
rolloRunter = 11

# Times (in sec)
timeRauf = 30
timeRunter = 30

# only one of following:
PULL = GPIO.PUD_DOWN    #GPIO -> GND
#PULL = GPIO.PUD_UP        #GPIO -> 3V3

# to use RaspberryPi gpio numbers
GPIO.setmode(GPIO.BCM)

#------------------------------------------------------------------------

# set up GPIO input channels
GPIO.setup(tasterRauf, GPIO.IN, pull_up_down = PULL)
GPIO.setup(tasterRunter, GPIO.IN, pull_up_down = PULL)

# set up GPIO output channels
GPIO.setup(rolloRauf, GPIO.OUT)
GPIO.setup(rolloRunter, GPIO.OUT)

# http://www.tutorialspoint.com/python/python_dictionary.htm
status = {}
status[rolloRauf] = 0
status[rolloRunter] = 0

def timedRequest(pin):
    print "{} wird abgeschaltet".format(pin)
    GPIO.output(pin, False)
    status[pin] = 0

def interrupt_event(pin):
    if pin == tasterRauf and not (status[rolloRauf] == 1) and not (status[rolloRunter] == 1):
        print "Fahre Rollo rauf"
        GPIO.output(rolloRauf, True)
        status[rolloRauf] = 1
        t = threading.Timer(timeRauf, timedRequest, rolloRauf)
        t.start() # after ... seconds "timedRequest" will be executed
    elif pin == tasterRunter and not (status[rolloRunter] == 1) and not (status[rolloRauf] == 1):
        print "Fahre Rollo runter"
        GPIO.output(rolloRunter, True)
        status[rolloRunter] = 1
        t = threading.Timer(timeRunter, timedRequest, rolloRunter)
        t.start() # after ... seconds "timedRequest" will be executed

try:
    GPIO.add_event_detect(tasterRauf, GPIO.RISING, callback=interrupt_event, bouncetime=150)
    GPIO.add_event_detect(tasterRunter, GPIO.RISING, callback=interrupt_event, bouncetime=150)

    #keep script running
    signal.pause()
except (KeyboardInterrupt, SystemExit):
    GPIO.cleanup()
    print "\nQuit\n"