#!/usr/bin/python
#
# v0.3 (c) by meigrafd
#
import RPi.GPIO as GPIO
import time, curses

#---------------------------------------------------------------------
# only one of following:
PULL = GPIO.PUD_DOWN	#GPIO -> GND
#PULL = GPIO.PUD_UP		#GPIO -> 3V3
#---------------------------------------------------------------------

RPv = GPIO.RPI_REVISION
if RPv == 1:
	GPIOpins = [0,1,4,17,21,22,10,9,11,14,15,18,23,24,25,8,7]
elif RPv == 2:
	GPIOpins = [2,3,4,17,27,22,10,9,11,14,15,18,23,24,25,8,7]
elif RPv == 3:
	GPIOpins = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,14,15,18,23,24,25,8,7,12,16,20,21]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for gpin in GPIOpins:
	GPIO.setup(gpin, GPIO.IN, pull_up_down = PULL)

def Interrupt_event(pin):
	global stdscr
	stdscr.addstr(1+pin, 5, ""+time.strftime("%d.%m.%Y %H:%M:%S")+" -> GPIO "+str(pin)+" ausgeloest!")
	stdscr.refresh()
	
def _exit():
	stdscr.keypad(0)
	curses.nocbreak()
	curses.echo()
	curses.endwin()
	GPIO.cleanup()

try:
	#for KeyPress Events
	stdscr = curses.initscr() #init curses
	curses.cbreak() #react on keys instantly without Enter
	curses.noecho() #turn off echoing of keys to the screen
	stdscr.keypad(1) #returning a special value such as curses.KEY_LEFT
	stdscr.addstr(0, 0, "Hit 'q' to quit") #display text on pos y, x
	for gpin in GPIOpins:
		GPIO.add_event_detect(gpin, GPIO.RISING, callback=Interrupt_event, bouncetime=100)
	running = True
	while running:
		key = stdscr.getch()
		stdscr.refresh()
		if key == ord('q'): raise KeyboardInterrupt
except KeyboardInterrupt:
	stdscr.addstr(1, 0, "..Quitting..")
	stdscr.refresh()
	running = False
	_exit()
except Exception, e:
	print("\nError: " + str(e))
	running = False
	_exit()