#!/usr/bin/python
#
# http://www.forum-raspberrypi.de/Thread-python-tkinter-mainloop-unterbrechen?pid=245488#pid245488
#
import Tkinter as tkinter
import random

class GUI(object):
    def __init__(self, resolution="300x200"):
        self.resolution = resolution
        self.running = False
        self.master = tkinter.Tk()
        self.Value = tkinter.IntVar()
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
    
    def run(self):
        self.master.geometry(self.resolution)
        self.Value_label = tkinter.Label(master=self.master)
        self.Value_label.configure(font=("Courier", 30), bg="steel blue", fg="red", textvariable = self.Value)
        self.Value_label.place(x=10, y=10, height=50, width=50)
        self.startstop_button = tkinter.Button(master=self.master, bg="#229", fg="white", text="Stop", command=self.startstop_func)
        self.startstop_button.place(x=150, y=10, height=50, width=50)
        self.exit_button = tkinter.Button(master=self.master, bg="indian red", fg="white", text="Exit", command=self.quit)
        self.exit_button.place(x=150, y=70, height=50, width=50)
        self.running = True
        self.master.after(500, self.changeValue)
        self.master.mainloop()
    
    def changeValue(self):
        value = random.randint(0, 300)
        self.Value.set(value)
        if self.running:
            self.master.after(500, self.changeValue)
    
    def startstop_func(self):
        if self.running == True:
            self.startstop_button["text"] = "Run"
            self.running = False
        else:
            self.startstop_button["text"] = "Stop"
            self.running = True
            self.changeValue()
    
    def quit(self):
        self.master.destroy()
        print("Quit")

try:
    app = GUI("200x150+10+10").run()
except KeyboardInterrupt:
    try: app.quit()
    except: pass
    
#EOF