#
# alternative:
# http://stackoverflow.com/questions/1918005/making-python-tkinter-label-widget-update
# http://effbot.org/tkinterbook/label.htm
#
#try:
	#python3
#	import tkinter
#except ImportError:
	#python2
#	import Tkinter as tkinter

from Tkinter import *
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)

tk = Tk()

def Interrupt_event(pin):
  global MyLabel1
  if GPIO.input(27): # if 27 == 1
    print("Rising edge detected on %s"%pin)
    MyLabel1["text"] = "Schalter ist aus"
  else: # if 27 != 1
    print("Falling edge detected on %s"%pin)
    MyLabel1["text"] = "Schalter ist an"

GPIO.add_event_detect(27, GPIO.BOTH, callback=Interrupt_event)

MyLabel1 = Label(tk, text="Schalter GPIO 27")
MyLabel1.grid(row=4, column=1)
MyLabel1.pack()

tk.mainloop()