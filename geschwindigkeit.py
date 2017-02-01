#!/usr/bin/python3
#
# http://www.forum-raspberrypi.de/Thread-python-geschwindigkeit-mit-gpio-impuls-berechnen?pid=127665#pid127665
# http://www.forum-raspberrypi.de/Thread-python-kmh-berechnung-fahrradcomputer?pid=260821#pid260821
# http://www.forum-raspberrypi.de/Thread-python-canvas-tachoanzeige?pid=254406#pid254406
#
import time
from RPi import GPIO

#---------------------------------
gpioPin = 22
#---------------------------------

# setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


range = 0.33 # wheel scope * pi
impuls = 0
rotations = 0
timeout = 5 #sec

#---------------------------------


def getDistance():
    return rotations * range


def getSpeed():
    speed = getDistance() / stamptime    # Geschwindigkeit = Stecke / Zeit
    return round(speed, 1)


def outputData():
    print "------------------------------------------"
    print("Zeit: {}".format(stamptime))
    print("rotations: {} pcs".format(rotations))
    print("Geschw: {} m/min".format(getSpeed()))
    print("Strecke: {} m".format(getDistance()))
    print "------------------------------------------"


def interrupt_event(channel):
    global rotations, impuls, timeStart
    rotations += 1
    impuls += 1
    timeEnd = time.time()
    if (time.time() - timeEnd) >= timeout:
        rotations = 0
    if impuls == 1:
        timeStart = time.time()


try:
    GPIO.add_event_detect(gpioPin, GPIO.RISING, callback=interrupt_event, bouncetime=100)
    
    while True:
        if impuls >= 3:
            impuls = 0
            stamptime = timeEnd - timeStart
            outputData()
        time.sleep(1)
    
except (KeyboardInterrupt, SystemExit):
    print("\nSchliesse Programm..\n")

#EOF