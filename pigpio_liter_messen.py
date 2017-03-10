#!/usr/bin/python3
#

from functools import partial
from queue import Queue
from time import time
import pigpio
import sqlite3


# ISR
def interrupt_Event(queue, gpio, level, tick):
    queue.put( int(time()) )


def main(gpioPin):
    amount = 0
    queue = Queue()
    gpio = pigpio.pi()
    gpio.set_mode(gpioPin, pigpio.INPUT)
    #gpio.set_pull_up_down(gpioPin, pigpio.PUD_UP)   #GPIO -> 3V3
    gpio.callback(gpioPin, pigpio.RISING_EDGE, partial(interrupt_Event, queue))
    
    try:
        connection = sqlite3.connect("/dev/shm/test.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY,amount VARCHAR(30),timestamp INT(11));")

        # 1 Liter = 100 impulse
        # 1 impuls = 10ml
        while True:
            stamp = queue.get()   # blockiert bis Eintrag im queue vorhanden
            amount += 10
            cursor.execute( "INSERT INTO test (amount,timestamp) VALUES (?,?,?)", (amount,stamp) )
    
    except (KeyboardInterrupt, SystemExit):
        gpio.stop()
        try: cursor.close()
        except: pass
        try: connection.close()
        except: pass
        print('\nQuit\n')


if __name__ == '__main__':
    main(gpioPin=17)


#EOF