# http://www.forum-raspberrypi.de/Thread-gpio-rpi-gpio-verliert-einstellung-gpio-setmode-und-gpio-setup
from RPi import GPIO
import threading
import os.path
import time


class watch(threading.Thread):
    def __init__(self, path, led_pin):
        threading.Thread.__init__(self)
        self.mounted = False
        self.path = path
        self.led_pin = led_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def run(self):
        while True:
            if (os.path.ismount(self.path)):
                self.mounted = True
                GPIO.output(self.led_pin, GPIO.HIGH)
            else:
                self.mounted = False
                GPIO.output(self.led_pin, GPIO.LOW)
            time.sleep(0.1)


class usbstick():
    def __init__(self, path, led_pin):
        self.timeout = 120
        self.path = path
        self.led_pin = led_pin
        self.usb_busy = threading.Lock()
        self.watch_thread = watch(self.path, self.led_pin)
        self.watch_thread.start()
    
    def ismounted(self):
        return self.watch_thread.mounted
    
    def waitmount(self):
        timestamp = time.time()
        while not self.ismounted():
            time.sleep(1)
            if ((time.time() - timestamp) > self.timeout):
                print 'Timeout.'
                time.sleep(5)
                #reboot()
                #myexit()
                return False
        print 'Massenspeichergeraet gefunden.'
        return True


if __name__ == "__main__":
    usbWatch = usbstick("/media/usb1", 17).waitmount()