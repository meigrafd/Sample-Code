import threading

class PeriodicExecutor(threading.Thread):
    def __init__(self, interval, func, **kwargs):
        """ Execute func(params) every 'interval' seconds """
        threading.Thread.__init__(self, name="PeriodicExecutor")
        self.setDaemon(1)
        self._finished = threading.Event()
        self._interval = interval
        self._func = func
        self._params = kwargs
        self.start()
    
    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval
    
    def shutdown(self):
        """Stop this thread"""
        self._finished.set()
    
    def run(self):
        while 1:
            if self._finished.isSet(): return
            self._func(**self._params)
            # sleep for interval or until shutdown
            self._finished.wait(self._interval)


#
## Example 1:
#

import time

def schreib(text):
    print(text)

one = PeriodicExecutor(5, schreib, text="Hallo Welt!")
time.sleep(5)
one.setInterval(10)

two = PeriodicExecutor(2, schreib, text="bla")
time.sleep(4)
two.setInterval(3)

three = PeriodicExecutor(5, schreib, text="Bye!")
time.sleep(5)

one.shutdown()
two.shutdown()
three.shutdown()

time.sleep(2)
print("Quit")



#
## Example 2:
#

import signal   

def schreib(text):
    print(text)

one = PeriodicExecutor(5, schreib, text="Hallo Welt!")
two = PeriodicExecutor(2, schreib, text="bla")
three = PeriodicExecutor(5, schreib, text="Bye!")

try: signal.pause()
except KeyboardInterrupt: pass

one.shutdown()
two.shutdown()
three.shutdown()

print("Quit")


#EOF