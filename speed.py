#!/usr/bin/python
import urllib2
import time
import contextlib
from datetime import datetime

# Download Geschwindigkeit messen
def measure(url="http://www.speedtestx.de/testfiles/data_500mb.test", intervall=2, buf=1024):
    with contextlib.closing(urllib2.urlopen(url)) as f:
        tStart = datetime.now()
        amount = 0
        while len(f.read(buf)) == buf is not None:
            tEnd = datetime.now()
            diff = (tEnd - tStart).total_seconds()
            if (diff > intervall):
                print "%s; %s MBit/s, %s amount, %s diff, %s buf" % ( time.strftime("%H:%M:%S"), (((amount/intervall)/1024.00)*8)/1024, amount, diff, buf)
                amount = 0
                tStart = datetime.now()
            else:
                amount = amount + buf

try:
    while True:
        measure()
except KeyboardInterrupt:
    pass