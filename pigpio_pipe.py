#!/usr/bin/python3
#
# by meigrafd
#
import sys

def writeGpio(mode,pin,type):
    try:
        handle = open("/dev/pigpio", "rb")
    except IOError as e:
        print("ERROR opening /dev/pigpio: %s" % e)
        handle = None
    if handle is not None:
        chunk = handle.read(12)
        
        f.close()