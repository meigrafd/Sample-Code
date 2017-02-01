#!/usr/bin/python
# by meigrafd
# http://www.forum-raspberrypi.de/Thread-python-netzwerk-traffic-von-wlan0-anzeigen?pid=153960#pid153960
#

from __future__ import print_function
import time, psutil, curses

try:
	running=True
	stdscr = curses.initscr() #init curses and create window object stdscr
	while running:
		c=1
		network_devices = psutil.network_io_counters(pernic=True)
		for device in network_devices:
			received = round( (float(network_devices[device].bytes_recv) / 1024.0) / 1024, 2)
			send = round( (float(network_devices[device].bytes_sent) / 1024.0) / 1024, 2)
			stdscr.addstr(c, 5, "{0:5} -> received: {1:10} MB send: {2:10} MB".format(device, received, send))
			stdscr.move(0,0) #move cursor to (new_y, new_x)
			stdscr.refresh() #update the display immediately
			c+=1
		time.sleep(0.1)

except KeyboardInterrupt:
	stdscr.addstr(0, 0, "..Quitting..")
	stdscr.refresh()
except Exception, e:
	print("\nError: " + str(e))

curses.endwin()
running=False
