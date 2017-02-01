#!/usr/bin/python2
#

from __future__ import print_function
from functools import partial
from Queue import Queue
from time import strftime
import pigpio


# ISR
def interrupt_Event(queue, gpio, level, tick):
    # gpio: the gpio number of event
    # level: 0 or 1
    # tick: the number of microseconds since system boot
    queue.put( (gpio, level) )   # tuple of channel and HIGH/LOW


def main():
    gpio_list = [2, 3, 4, 17, 27, 22, 10, 9, 11, 18, 23, 24, 25, 8, 7]
    queue = Queue()
    gpio = pigpio.pi()
    
    # Interrupt Event fuer jeden gpio hinzufuegen.
    for pin in gpio_list:
        gpio.set_mode(pin, pigpio.INPUT)
        #gpio.set_pull_up_down(pin, pigpio.PUD_UP)   #GPIO -> 3V3
        gpio.callback(pin, pigpio.EITHER_EDGE, partial(interrupt_Event, queue))
    
    try:
        # Queue abarbeiten
        while True:
            pin, state = queue.get()   # blockiert bis Eintrag im queue vorhanden
            if state == pigpio.LOW:
                print("{} Falling edge detected on {}".format(strftime("%d.%m.%Y %H:%M:%S"), pin))
            elif state == pigpio.HIGH:
                print("{} Rising edge detected on {}".format(strftime("%d.%m.%Y %H:%M:%S"), pin))
    
    except (KeyboardInterrupt, SystemExit):
        gpio.stop()
        print('\nQuit\n')


if __name__ == '__main__':
    main()


#EOF