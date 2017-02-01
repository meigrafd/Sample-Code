#!/usr/bin/python2.7
import re
import time

# define path to 1-wire sensor
pathes = (
	"/sys/bus/w1/devices/10-000801b5a7a6/w1_slave",
	"/sys/bus/w1/devices/10-000801b5959d/w1_slave"
)

def read_sensor(path):
	value=None
	try:
		with open(path, 'r') as fd:
            line = fd.readline()
            if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
                line = fd.readline()
                m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
                if m:
                    value = str(float(m.group(2)) / 1000.0)
	except (IOError), e:
		print time.strftime("%x %X"), "Error reading", path, ": ", e
	return value

# read sensor data
for path in pathes:
	data = read_sensor(path)
	if data:
		print '{} -> {}'.format(path, data)
	else:
		print '{} -> None'.format(path)
	time.sleep(1)
