from __future__ import print_function
import RPi.GPIO as GPIO
import time, threading
try:
    #python3
    import tkinter
except ImportError:
    #python2
    import Tkinter as tkinter
#------------------------------------------------------------------------
# using an list to hold the gpio numbers
gpioList = [11, 12, 13, 15]

steps = [
    [0,0,0,0],
    [0,0,0,1],
    [0,0,1,0],
    [0,0,1,1],
    [0,1,0,0],
    [0,1,0,1],
    [0,1,1,0],
    [0,1,1,1],
    [1,0,0,0],
    [1,0,0,1]
]

# define dictionary http://www.tutorialspoint.com/python/python_dictionary.htm
dictionary = {}
dictionary['sleep'] = 2
dictionary['running'] = False
#------------------------------------------------------------------------

# Initializes the GPIO pins
GPIO.setmode(GPIO.BOARD)
for pin in gpioList:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

def schleife():
    while dictionary['running'] == True:
        for stepIdx in range(0, len(steps)):
            if dictionary['running'] == False:
                break
            print("schritt: %d" % stepIdx)
            for pinIdx in range(0, len(steps[stepIdx])):
                GPIO.output(gpioList[pinIdx], steps[stepIdx][pinIdx])
            time.sleep( float(dictionary['sleep']) )

def _exit():
    dictionary['running'] = False
    GPIO.cleanup()

def set_sleepTime():
    print("Sleepzeit: %s" % sleepTimeEntry.get())
    dictionary['sleep'] = sleepTimeEntry.get()

def set_StartStop():
    print(StartStopButton['text'])
    # if button got pressed and currently text is 'Start' then start loop thread and change button text..
    if StartStopButton['text'] == "Start":
        dictionary['running'] = True
        StartStopButton['text'] = "Stop"
        schleife_thread = threading.Thread(target=schleife)
        schleife_thread.start()
    elif StartStopButton['text'] == "Stop":
        dictionary['running'] = False
        StartStopButton['text'] = "Start"

try:
    master = tkinter.Tk()
    sleepTimeLabel = tkinter.Label(master, text="Zeit in Sek").grid(row=0)
    sleepTimeEntry = tkinter.Entry(master)
    sleepTimeEntry.grid(row=0, column=1)
    sleepTimeEntry.insert(0, dictionary['sleep'])
    sleepTimeEntry.focus_set()
    sleepTimeButton = tkinter.Button(master, text='Set', command=set_sleepTime)
    sleepTimeButton.grid(row=3, column=1, sticky=tkinter.W, pady=4)
    StartStopButton = tkinter.Button(master, text='Start', command=set_StartStop)
    StartStopButton.grid(row=3, column=2, sticky=tkinter.W, pady=4)
    master.mainloop()
except (KeyboardInterrupt, SystemExit):
    print("\nschliesse Programm...\n")
    _exit()

_exit()
