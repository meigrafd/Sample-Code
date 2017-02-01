#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
try:
    #python3
    import tkinter
except ImportError:
    #python2
    import Tkinter as tkinter
 
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
 
fenster = tkinter.Tk()
fenster.title ("LED an aus")
fenster.geometry("640x480")
photo = tkinter.PhotoImage(file="/tmp/LED.gif")
label = tkinter.Label(master=fenster, image=photo)
label.image = photo
label.pack()

def LED1():
    if GPIO.input(25):
        print("Aus")
        GPIO.output(25, False)
    else:
        print("An")
        GPIO.output(25, True)
 
#Buttons erstellen und platzieren
B1 = tkinter.Button(fenster, bg="white", text="LED_1", command=LED1)
B1.place (x=450, y=50)
 
try:
    fenster.mainloop()
except (KeyboardInterrupt, SystemExit):
    print("schliesse Programm...")
 
GPIO.cleanup()
