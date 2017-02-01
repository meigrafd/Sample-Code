#!/usr/bin/python3
# coding: utf-8
import time
from tkinter import *
import os
#-------------------------------------------------------------------------    
def keyup(e):
    print ("STOP")

def keydown(e):
    key = e.keysym
    if key == "Up":
        print ("Vorwaerts")
    elif key == "Down":
        print ("Rueckwaerts")
    elif key == "Left":
        print ("Links")
    elif key == "Right":
        print ("Rechts")
#-------------------------------------------------------------------------
os.system('xset r off')
root = Tk()
frame = Frame(root, width=600, height=400)
frame.bind("<KeyPress>", keydown)
frame.bind("<KeyRelease>", keyup)
frame.pack()
frame.focus_set()
root.mainloop()

