#
# http://www.forum-raspberrypi.de/Thread-python-taster-funktion-schleife-beenden?page=2
#
import RPi.GPIO as GPIO
import time
import signal
import threading

#------------------------------------------------------------------------
# use the raspi board pin number
#GPIO.setmode(GPIO.BOARD)
# use the gpio number
GPIO.setmode(GPIO.BCM)

# only one of following for GPIO.IN:
PULL = GPIO.PUD_DOWN  #GPIO -> GND
#PULL = GPIO.PUD_UP   #GPIO -> 3V3

Taster = 17
#------------------------------------------------------------------------

GPIO.setup(Taster, GPIO.IN, pull_up_down=PULL)

def cputemp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        CPUtemp = int(float(f.readline().split()[0]))
        CPUtemp = round((CPUtemp/1000.0), 2)
    return CPUtemp

def TimedRequest(when, what):
    global timed
    when = float(when)
    what = str(what)
    zeit = time.strftime("%d.%m.%Y %H:%M:%S")
    if what == "pitemp":
        print "{} --> {}".format(zeit, cputemp())
    timed = threading.Timer( when, TimedRequest, [when, what] )
    timed.start() 

def interrupt_event(pin):
    global timed
    if GPIO.input(Taster) == GPIO.HIGH:
        if not timed:
            timed = threading.Timer( 1.0, TimedRequest, ["1.0", "pitemp"] )
            timed.start()
        else:
            timed.cancel()
            timed = False

if __name__ == '__main__':
    try:
        timed = False
        GPIO.add_event_detect(Taster, GPIO.BOTH, callback=interrupt_event, bouncetime=150)
        #keep script running
        signal.pause()
    except (KeyboardInterrupt, SystemExit):
        print "\nQuit\n"
        GPIO.cleanup()
        if timed:
                timed.cancel()