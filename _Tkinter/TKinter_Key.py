#!/usr/bin/python3
# coding: utf-8
import RPi.GPIO as GPIO
import time
from tkinter import *
import os
#------------------------------------------------------------------------
# Setmode
GPIO.setmode(GPIO.BCM)
# Setwarning deaktivieren
GPIO.setwarnings(False)
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
# Pin definition
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
#------------------------------------------------------------------------
# Antriebe stoppen
def motor_stop():
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)
#-------------------------------------------------------------------------
def forward():
    GPIO.output(IN1, True) # Motor A (links) vorwaerts
    GPIO.output(IN2, False)
    GPIO.output(IN3, True) # Motor B (rechts) vorwaerts
    GPIO.output(IN4, False)

def backward():
    GPIO.output(IN1, False)
    GPIO.output(IN2, True) # Motor A (links) rueckwaerts
    GPIO.output(IN3, False)
    GPIO.output(IN4, True) # Motor B (rechts) rueckwaerts
def left():
    GPIO.output(IN1, True) # Motor A (links) vorwaerts
    GPIO.output(IN2, False)
    GPIO.output(IN3, False) # Motor B (rechts) aus
    GPIO.output(IN4, False)
def right():
    GPIO.output(IN1, False) # Motor A (links) aus
    GPIO.output(IN2, False)
    GPIO.output(IN3, True) # Motor B (rechts) vorwaerts
    GPIO.output(IN4, False)
#-------------------------------------------------------------------------    
def keyup(e):
    motor_stop()
    print ("STOP")

def keydown(e):
    key = e.keysym
    if key == "Up":
        forward()
        print ("Vorwaerts")
    elif key == "Down":
        backward()
        print ("Rueckwaerts")
    elif key == "Left":
        right()
        print ("Links")
    elif key == "Right":
        left()
        print ("Rechts")
#-------------------------------------------------------------------------
os.system('xset r off')
GPIO.output(ENA, True)
GPIO.output(ENB, True)
root = Tk()
frame = Frame(root, width=600, height=400)
frame.bind("<KeyPress>", keydown)
frame.bind("<KeyRelease>", keyup)
frame.pack()
frame.focus_set()
root.mainloop()

