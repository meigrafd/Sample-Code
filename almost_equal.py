#!/usr/bin/python3.5
#
# http://www.forum-raspberrypi.de/Thread-python-temperaturkurve-in-python-umsetzen?pid=271983#pid271983
#
import time
import math
import random

stufen = {
    2: -1,
    10: -5,
    40: -15,
    -5: +2,
}

toleranz = 3

def _Temp():
    return random.randint(-10, 60)

while True:
    time.sleep(2)
    actualTemp = _Temp()
    print("Aktuelle Temperatur: %s" % actualTemp)
    for step in stufen:
        if math.isclose(actualTemp, step, abs_tol=toleranz):
            print("Stufe: %s ... Senke um: %s " % (step, stufen[step]))
    
#EOF