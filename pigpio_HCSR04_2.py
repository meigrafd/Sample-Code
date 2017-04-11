#!/usr/bin/python3
import pigpio
import time

timeout = 2100  # Number of loop iterations before timeout called
GPIO_TRIGGER = 20
GPIO_ECHO = 21


def measure():
    countdown=timeout
    gpio.write(GPIO_TRIGGER, pigpio.HIGH)
    time.sleep(0.00001)
    gpio.write(GPIO_TRIGGER, pigpio.LOW)
    StartZeit = time.time()
    StopZeit = time.time()
    
    while (gpio.read(GPIO_ECHO) == 0 and countdown > 0):
        countdown -= 1
    
    if countdown > 0:
        StartZeit = time.time()
        countdown=timeout
        while (gpio.read(GPIO_ECHO) == 1 and countdown > 0):
            countdown -= 1
        StopZeit = time.time()
        TimeElapsed = StopZeit - StartZeit
    
    if countdown > 0:
        distance = (TimeElapsed*1000000)/58
        return distance
    else:
        print("Distance - timeout")
        return False ### This should indicate that the distance has timed out.


def measure_average(count=3):
    c=1
    distance=0
    while (c <= count):
        dest = measure()
        if dest:
            distance = distance + dest
            time.sleep(0.1)
            c+=1
    return distance / count


if __name__ == '__main__':
    try:
        gpio = pigpio.pi()
        gpio.set_mode(GPIO_TRIGGER, pigpio.OUTPUT)
        gpio.set_mode(GPIO_ECHO, pigpio.INPUT)
        while True:
            distance = measure_average()
            print("Gemessene Entfernung = %.1f cm" % distance)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        gpio.stop()


#EOF
