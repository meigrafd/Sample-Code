#!/usr/bin/python2
# coding: utf-8
from __future__ import print_function
import pigpio
import time
from Tkinter import *
import os
#------------------------------------------------------------------------
# Pins

# Motor A (links)
IN1 = 12
IN2 = 16
# Motor B (rechts)
IN3 = 24
IN4 = 25
# Enable der Motoren
ENA = 20
ENB = 21

#------------------------------------------------------------------------
def gpio_init():
    pi.set_mode(IN1, pigpio.OUTPUT)
    pi.set_mode(IN2, pigpio.OUTPUT)
    pi.set_mode(IN3, pigpio.OUTPUT)
    pi.set_mode(IN4, pigpio.OUTPUT)
    pi.set_mode(ENA, pigpio.OUTPUT)
    pi.set_mode(ENB, pigpio.OUTPUT)
#------------------------------------------------------------------------
# Antriebe stoppen
def motor_stop():
    pi.write(IN1, False)
    pi.write(IN2, False)
    pi.write(IN3, False)
    pi.write(IN4, False)
#-------------------------------------------------------------------------
def forward():
    pi.write(IN1, True) # Motor A (links) vorwaerts
    pi.write(IN2, False)
    pi.write(IN3, True) # Motor B (rechts) vorwaerts
    pi.write(IN4, False)

def backward():
    pi.write(IN1, False)
    pi.write(IN2, True) # Motor A (links) rueckwaerts
    pi.write(IN3, False)
    pi.write(IN4, True) # Motor B (rechts) rueckwaerts

def left():
    pi.write(IN1, True) # Motor A (links) vorwaerts
    pi.write(IN2, False)
    pi.write(IN3, False) # Motor B (rechts) aus
    pi.write(IN4, False)

def right():
    pi.write(IN1, False) # Motor A (links) aus
    pi.write(IN2, False)
    pi.write(IN3, True) # Motor B (rechts) vorwaerts
    pi.write(IN4, False)
#-------------------------------------------------------------------------    
def keyup(e):
    print("STOP")
    motor_stop()

def keydown(e):
    key = e.keysym
    if key == "Up":
        print("Vorwaerts")
        forward()
    elif key == "Down":
        print("Rueckwaerts")
        backward()
    elif key == "Left":
        print("Links")
        left()
    elif key == "Right":
        print("Rechts")
        right()
#-------------------------------------------------------------------------
try:
    pi = pigpio.pi() #accesses the local Pi's gpios
    pigpio.exceptions = False
    gpio_init()
    os.system('xset r off')
    pi.write(ENA, True)
    pi.write(ENB, True)
    root = Tk()
    frame = Frame(root, width=600, height=400)
    frame.bind("<KeyPress>", keydown)
    frame.bind("<KeyRelease>", keyup)
    frame.pack()
    frame.focus_set()
    root.mainloop()
except KeyboardInterrupt:
    print("\nQuit\n")
    pi.stop()
except Exception, e:
    print("\nError: " + str(e))
    pi.stop()