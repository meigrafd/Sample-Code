# Threading Beispiel für python 3
from queue import Queue
from threading import Thread
from time import sleep
from time import localtime

def printInfo(in_q):
    while True:
        while in_q.empty() == False:
            print("Inhalt Queue: " + str(in_q.get()))
        sleep(0.1)

def measure(foo, out_q):
    while True:
        q.put(foo + str(localtime()[5]))
        sleep(2)

q = Queue()
measure_t = Thread(target=measure, args=("test", q,))
print_t = Thread(target=printInfo, args=(q,))
measure_t.start()
print_t.start()