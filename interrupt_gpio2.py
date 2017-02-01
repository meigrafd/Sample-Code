import time
from time import *
import RPi.GPIO as GPIO

gpioPin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

zielwert = 20
log = "logdatei.txt"
CounterUP = 0
finished = False

def Interrupt_event(pin):
  global CounterUP
  if GPIO.input(gpioPin): # if gpioPin == 1
    print("Rising edge detected on %s"%pin)
    CounterUP = (CounterUP + 1)
  if CounterUP >= zielwert:
    CounterUP = 0
    print("speichern")
    datum = strftime("%d.%m.%Y")
    zeit = strftime("%H.%M.%S")
    with open(log, 'a') as f:
        f.write(datum +", "+ zeit +"\n")
  print("CounterUP: %s" % CounterUP)

try:
  print("Starte Program")
  GPIO.add_event_detect(gpioPin, GPIO.BOTH, callback=Interrupt_event, bouncetime=200)
  while not finished:
    time.sleep(1)
      
except KeyboardInterrupt:
  finished = True
  print("Quit")
GPIO.cleanup()