#!/usr/bin/python
from datetime import datetime
from datetime import timedelta

#every = 4.9578 # ms
every = 120

# returns the elapsed milliseconds since the start of the program
def millis():
    dt = datetime.now() - start_time 
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0 
    return ms 

start_time = datetime.now()
pingTimer = 0

while True:
    if millis() >= pingTimer:
        pingTimer += every
        print pingTimer