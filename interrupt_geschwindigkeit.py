#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import signal

#---------------------------------
gpioPin = 22
#---------------------------------

# setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Variablen
section = 0.33
impuls = 0
totalImpuls = 0

#---------------------------------

def getSect():
	sect = totalImpuls * section
	return sect

def getTime():
	stamptime = (timeEnd - timeStart) / 60
	return stamptime
    
def getSpeed():
	speed = section / getTime()    # Geschwindigkeit = Weg / Zeit
	speed = round(speed,1)
	return speed

def outputData():
	stamptime = str(getTime())
	print timeStart
	print timeEnd
	print stamptime
	print "------------------------------------------"
	print("Zeit: " + stamptime)
	print("TotalImpuls: {} pcs".format(totalImpuls))
	print("Geschw: " + format(getSpeed()) + " m/min")
	print("Strecke: {} m".format(getSect()))
	print "------------------------------------------"

def Interrupt(channel):
	global totalImpuls, impuls, timeStart, timeEnd
	totalImpuls = int(totalImpuls + 1)
	impuls = int(impuls + 1)
	if impuls == 1:
		timeStart = time.time()
	elif impuls == 3:
		impuls = 0
		timeEnd = time.time()
		outputData()

try:
	GPIO.add_event_detect(gpioPin, GPIO.RISING, callback=Interrupt, bouncetime=100)
	#keep script running
	signal.pause()
except (KeyboardInterrupt, SystemExit):
	print("\nSchliesse Programm..\n")
