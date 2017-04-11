#!/usr/bin/python3
#
# http://www.forum-raspberrypi.de/Thread-python-ultraschallsensor-code-mit-rpi-gpio-geht-mit-pigpio-nicht
#
import pigpio
import time


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