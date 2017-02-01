#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import queue as Queue # https://pymotw.com/2/Queue/
from functools import partial
from threading import Thread

#------------------------------------------------------------------------
# use the raspi board pin number
#GPIO.setmode(GPIO.BOARD)
# use the gpio number
GPIO.setmode(GPIO.BCM)

Taster = 25

#------------------------------------------------------------------------

def interrupt_event(qF, qR, pin):
    if GPIO.input(pin) == GPIO.HIGH:
        qR.put(pin)
    else:
        qF.put(pin)

def rising_edge(queue):
    while running:
        if not queue.empty():
            pin = queue.get()
            zeit = time.strftime("%d.%m.%Y %H:%M:%S")
            print("{} Rising edge detected on {}".format(zeit, pin))
        time.sleep(0.5)

def falling_edge(queue):
    while running:
        if not queue.empty():
            pin = queue.get()
            zeit = time.strftime("%d.%m.%Y %H:%M:%S")
            print("{} Falling edge detected on {}".format(zeit, pin))
        time.sleep(0.5)

def main():
    queueFalling = Queue.Queue()
    queueRising = Queue.Queue()
    rising_thread = Thread(target=rising_edge, args=(queueRising,))
    falling_thread = Thread(target=falling_edge, args=(queueFalling,))
    rising_thread.start()
    falling_thread.start()
    GPIO.setup(Taster, GPIO.IN)
    GPIO.add_event_detect(Taster, GPIO.BOTH, callback=partial(interrupt_event, queueFalling, queueRising), bouncetime=200)
    #keep script running
    while True:
        time.sleep(5)


if __name__ == '__main__':
    try:
        running = True
        main()
    except (KeyboardInterrupt, SystemExit):
        running = False
        print("\nQuit\n")
        GPIO.cleanup()