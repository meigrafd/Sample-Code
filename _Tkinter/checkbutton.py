#!/usr/bin/python3
#
# http://www.forum-raspberrypi.de/Thread-python-tkinter-checkbutton-aktivieren?pid=223246#pid223246
#
from tkinter import *

master = Tk()

expand = IntVar()
expand.set(1)
c = Checkbutton(master, text="Erweitern", variable=expand)
c.pack()

expand2 = IntVar()
c2 = Checkbutton(master, text="Erweitern2", variable=expand2)
c2.select()
c2.pack()

master.mainloop()
