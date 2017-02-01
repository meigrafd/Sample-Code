#!/usr/bin/python
from __future__ import print_function
import RPi.GPIO as GPIO
import time
import Queue # https://pymotw.com/2/Queue/

#GPIO pins
Taster1 = 27

# GPIO-Nummer als Pinreferenz waehlen
GPIO.setmode(GPIO.BCM)  

# GPIO vom SoC als Input deklarieren und Pull-Down Widerstand aktivieren
#PULL = GPIO.PUD_DOWN    #GPIO -> GND
PULL = GPIO.PUD_UP        #GPIO -> 3V3
GPIO.setup(Taster1, GPIO.IN, pull_up_down=PULL)

# Dictionary definieren. http://www.tutorialspoint.com/python/python_dictionary.htm
dictionary = {}
dictionary['pause'] = False

queue = Queue.Queue()

# Script pausieren/blockieren/beschaeftigen
def Pause():
   while dictionary['pause'] == True:
       time.sleep(1)

# ISR
def Interrupt(pin):
    if pin == Taster1:
        if dictionary['pause'] == True:
            print("Fuehre Script weiter aus")
            dictionary['pause'] = False       
        else:
            queue.put(pin)

try:
    # Interrupt Event hinzufuegen. Auf steigende Flanke reagieren und ISR "Interrupt" deklarieren sowie Pin entprellen
    GPIO.add_event_detect(Taster1, GPIO.RISING, callback=Interrupt, bouncetime=200)
    # keep script running
    while True:
        time.sleep(0.5)
        if not queue.empty():
            job = queue.get()
            if job == Taster1:
                print("Pausiere Script")
                dictionary['pause'] = True
                Pause()
        print("...puh... Im super heavy busy...")
except (KeyboardInterrupt, SystemExit):
   GPIO.cleanup()
   print("\nQuit\n")