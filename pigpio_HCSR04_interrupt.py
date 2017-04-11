#!/usr/bin/python3
import pigpio
import time

timeout = 2100  # Number of loop iterations before timeout called

GPIO_TRIGGER = 20
GPIO_ECHO = 21

def _callback(gpio, level, tick):
    # gpio: the gpio number of event
    # level: 0 or 1
    # tick: the number of microseconds since system boot
    if gpio == self._trig:
        if level == 0: # trigger sent
            self._triggered = True
            self._high = None
    else:
        if self._triggered:
            if level == 1:
                self._high = tick
            else:
                if self._high is not None:
                    self._time = tick - self._high
                    self._high = None
                    self._ping = True

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


def measure_average():
    count = 1
    distance = 0
    while (count <= 3):
        distance = distance + measure()
        time.sleep(0.1)
        count = count + 1
    distance = distance / 3
    return distance


if __name__ == '__main__':
    try:
        gpio = pigpio.pi()
        gpio.set_mode(GPIO_TRIGGER, pigpio.OUTPUT)
        gpio.set_mode(GPIO_ECHO, pigpio.INPUT)
        while True:
            distance = measure_average()
            if not distance:
                print("Timeout")
            print("Gemessene Entfernung = %.1f cm" % distance)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        gpio.stop()


#EOF


class Sonar_Ranger(object):
    def __init__(self, gpio, trigger, echo):
        self.gpio = gpio
        self._trig = trigger
        self._echo = echo
        self._ping = False
        self._high = None
        self._time = None
        self._triggered = False
        self._timeout = 5.0
        self._trig_orig_mode = gpio.get_mode(self._trig)
        self._echo_orig_mode = gpio.get_mode(self._echo)
        gpio.set_mode(self._trig, pigpio.OUTPUT)
        gpio.set_mode(self._echo, pigpio.INPUT)
        self._callback = gpio.callback(self._trig, pigpio.EITHER_EDGE, self._callback_func)
        self._callback = gpio.callback(self._echo, pigpio.EITHER_EDGE, self._callback_func)
        self._inited = True
    
   def _callback_func(self, gpio, level, tick):
      if gpio == self._trig:
         if level == 0: # trigger sent
            self._triggered = True
            self._high = None
      else:
         if self._triggered:
            if level == 1:
               self._high = tick
            else:
               if self._high is not None:
                  self._time = tick - self._high
                  self._high = None
                  self._ping = True
    
   def read(self):
      """
      Triggers a reading.  The returned reading is the number of microseconds for the sonar round-trip.
      round trip cms = round trip time / 1000000.0 * 34030
      """
      if self._inited:
         self._ping = False
         self.gpio.gpio_trigger(self._trig)
         start = time.time()
         while not self._ping:
            if (time.time()-start) > self._timeout:
               return 20000
            time.sleep(0.001)
         return self._time
      else:
         return None
    
   def cancel(self):
      """
      Cancels the ranger and returns the gpios to their original mode.
      """
      if self._inited:
         self._inited = False
         self._callback.cancel()
         self.gpio.set_mode(self._trig, self._trig_orig_mode)
         self.gpio.set_mode(self._echo, self._echo_orig_mode)


if __name__ == '__main__':
    try:
        pi = pigpio.pi()
        sonar = Sonar_Ranger(pi, 23, 18)
        while True:
            print(sonar.read())
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nQuit\n")
        sonar.cancel()
        pi.stop()


#EOF