import pigpio
import time


GPIO_TRIGGER = 20
GPIO_ECHO = 21


def distance():
    gpio.write(GPIO_TRIGGER, pigpio.HIGH)
    time.sleep(0.00001)
    gpio.write(GPIO_TRIGGER, pigpio.LOW)
    StartZeit = time.time()
    StopZeit = time.time()
    while gpio.read(GPIO_ECHO) == 0:
        StartZeit = time.time()
    while gpio.read(GPIO_ECHO) == 1:
        StopZeit = time.time()
    TimeElapsed = StopZeit - StartZeit
    return (TimeElapsed * 34300) / 2


if __name__ == '__main__':
    try:
        gpio = pigpio.pi()
        gpio.set_mode(GPIO_TRIGGER, pigpio.OUTPUT)
        gpio.set_mode(GPIO_ECHO, pigpio.INPUT)
        while True:
            print("Gemessene Entfernung = %.1f cm" % distance())
            time.sleep(1)

    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        gpio.stop()


#EOF