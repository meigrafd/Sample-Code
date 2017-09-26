from RPi import GPIO
from time import sleep
from subprocess import call
from sys import exit
import shlex

import signal

def handler(signum, frame):
    exit()

signal.signal(signal.SIGINT, handler)

pwrLED=35
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwrLED, GPIO.IN)

lowPower=0
while True:
    if GPIO.input(pwrLED) == 0:
        call(shlex.split("echo -ne '\e[s''\e[1;56H''\e[1;31m'POWER dipped below 4.63V'\e[u''\e[0m'"))
        lowPower+=1
    else:
        lowPower=0
        call(shlex.split("echo -ne '\e[s''\e[1;78H''\e[1;31m'OK'\e[u''\e[0m'"))
    
    if lowPower  > 3:
        break
    
    sleep(1)

#call(shlex.split("echo -ne '\e[u''\e[0m'"))
print "Low power for " + str(lowPower) + " seconds"