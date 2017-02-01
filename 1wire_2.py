#!/usr/bin/python3
#
# print all available 1wire sensor values.
#
# Copyright (C) 2016 by meiraspi@gmail.com published under the MIT License
#
from sys import exit
import re
import os
import time


if os.path.isfile("/sys/bus/w1/devices/w1_bus_master1/w1_master_slave_count") == False:
    print("ERROR: w1 Kernel Module not loaded?")
    print("modprobe w1-gpio pullup=1")
    print("modprobe w1-therm")
    exit()

with open("/sys/bus/w1/devices/w1_bus_master1/w1_master_slave_count", "r") as fd:
    slave_count = fd.readline().rstrip('\n')
    #slave_count = [x.rstrip('\n') for x in fd.readlines()]
    if slave_count == 0:
        print("ERROR: No 1-wire Sensors connected?")
        exit()

def read_sensor(addr):
    path="/sys/bus/w1/devices/%s/w1_slave" % addr
    value=None
    try:
        with open(path, 'r') as fd:
            line = fd.readline()
            if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
                line = fd.readline()
                m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
                if m:
                    value = str(float(m.group(2)) / 1000.0)
    except (IOError) as e:
        print("{0} Error reading {1}: {2}".format(time.strftime("%x %X"), path, e))
    return value

# read each sensor data
with open("/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves", "r") as fd:
    w1_slave = [line.rstrip('\n') for line in fd]
    data = read_sensor(w1_slave)
    if data:
        print('{} -> {}'.format(w1_slave, data))
    else:
        print('{} -> None'.format(w1_slave))
    
