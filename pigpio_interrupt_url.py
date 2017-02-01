#!/usr/bin/python2
#
# http://www.forum-raspberrypi.de/Thread-gpio-status-in-mysql-datenbank-schreiben?pid=246631#pid246631
#

from __future__ import print_function
from functools import partial
from Queue import Queue
import pigpio
import requests


# ISR
def interrupt_Event(queue, gpio, level, tick):
    # gpio: the gpio number of event
    # level: 0 or 1
    # tick: the number of microseconds since system boot
    queue.put( (gpio, level) )   # tuple of channel and HIGH/LOW


def main():
    URL = 'http://192.168.178.103/middleware.php/data/{}.json?value={}'
    
    # (<gpio>, "<uuid>")
    pins_and_uuids = [
        (5, 'c8ef0690-993e-11e6-93bf-05928009d3e3'),
        (6, '6c63f740-94b6-11e6-8b55-15bb6ce24a5e'),
    ]
    
    queue = Queue()
    gpio = pigpio.pi()
    LOOKUP = dict()
    
    # Interrupt Event fuer jeden gpio hinzufuegen.
    for pin,uuid in pins_and_uuids:
        gpio.set_mode(pin, pigpio.INPUT)
        gpio.set_pull_up_down(pin, pigpio.PUD_UP)   #GPIO -> 3V3
        gpio.callback(pin, pigpio.EITHER_EDGE, partial(interrupt_Event, queue))
        for state,value in [(pigpio.LOW, 0), (pigpio.HIGH, 100)]:
            LOOKUP[(pin, state)] = URL.format(uuid, value)
    
    try:
        # Queue abarbeiten
        while True:
            url = LOOKUP[queue.get()]   # blockiert bis Eintrag im queue vorhanden
            requests.post(url)
    
    except (KeyboardInterrupt, SystemExit):
        print('\nQuit\n')


if __name__ == '__main__':
    main()


#EOF