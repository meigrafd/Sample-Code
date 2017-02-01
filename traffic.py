#!/usr/bin/python
#
# http://www.forum-raspberrypi.de/Thread-python-netzwerk-traffic-von-wlan0-anzeigen?pid=153960#pid153960
#

from __future__ import print_function
import psutil

network_devices = psutil.net_io_counters(pernic=True)

for device in network_devices:
	received = round( (float(network_devices[device].bytes_recv) / 1024.0) / 1024, 2)
	send = round( (float(network_devices[device].bytes_sent) / 1024.0) / 1024, 2)
	print("{0:4} -> received: {1:10}MB send: {2:10}MB".format(device, received, send))
