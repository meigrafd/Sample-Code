#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import curses
import RPi.GPIO as GPIO

#------------------------------------------------------------------------

red = 17
green = 22

# to use RaspberryPi gpio# (BCM) or pin# (BOARD)
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

#------------------------------------------------------------------------

GPIO.setwarnings(False)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

def schalten(pin):
    current_state = GPIO.input(pin)
    GPIO.output(pin, not current_state)
    stdscr.addstr(3, 5, 'switched GPIOpin {} from {} to {}' . format(pin, current_state, (not current_state)))

try:
    running=True
    #for KeyPress Events
    stdscr = curses.initscr() #init curses
    curses.cbreak() #react on keys instantly without Enter
    curses.noecho() #turn off echoing of keys to the screen
    stdscr.keypad(1) #returning a special value such as curses.KEY_LEFT
    stdscr.addstr(0, 0, "Hit 'q' to quit") #display text on pos y, x
    # run the loop
    while running:
        stdscr.move(1,0) #move cursor to (new_y, new_x)
        key = stdscr.getch() #waits until a key is pressed
        stdscr.clrtobot() #erase all lines below the cursor
        stdscr.refresh()
        if key == ord('q'): raise KeyboardInterrupt
        elif key == ord('a'):
            stdscr.addstr(2, 5, 'Key "a" is pressed')
            schalten(red)
        elif key == ord('1'):
            stdscr.addstr(2, 5, 'Key "1" is pressed')
            schalten(green)
        else:
            stdscr.addstr(2, 5, 'Unknown Key: "{}"'.format(curses.keyname(key)))
        stdscr.refresh()

except KeyboardInterrupt:
    stdscr.addstr(1, 0, "..Quitting..")
    stdscr.refresh()
    running=False
except Exception, e:
    print("\nError: " + str(e))
    running=False

stdscr.keypad(0)
curses.nocbreak()
curses.echo()
curses.endwin()
GPIO.cleanup()