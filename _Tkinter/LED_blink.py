#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# http://www.forum-raspberrypi.de/Thread-python-phyton-tkinter-gui-while-schleife-laesst-sich-nicht-beenden
#

from RPi import GPIO
try:
    # python3
    import tkinter as tk
except ImportError:
    # python2
    import Tkinter as tk


# GPIO Nummer verwenden
GPIO.setmode(GPIO.BCM)

LED_RED = 21       # Pin 40 (GPIO 21)

GPIO.setup(LED_RED, GPIO.OUT)


class MyApp(tk.Tk):
    def __init__(self):
        Tk.__init__(self)
        fr = tk.Frame(self)
        fr.pack()
        self.canvas  = tk.Canvas(fr, height=100, width=100)
        self.canvas.pack()
        self.rect = self.canvas.create_rectangle(25, 25, 75, 75, fill="white")
        self.do_blink = False
        start_button = tk.Button(self, text="start blinking", command=self.start_blinking)
        stop_button = tk.Button(self, text="stop blinking", command=self.stop_blinking)
        start_button.pack()
        stop_button.pack()
        self.text_label = tk.Label(self, text="Hallo")
        self.text_label.pack()
        GPIO.output(LED_RED, GPIO.HIGH)
    
    def start_blinking(self):
        self.do_blink = True
        self.blink()
    
    def stop_blinking(self):
        self.do_blink = False
    
    def blink(self):
        if self.do_blink:
            current_color = self.canvas.itemcget(self.rect, "fill")
            new_color = "red" if current_color == "white" else "white"
            self.canvas.itemconfigure(self.rect, fill=new_color)
            self.text_label.configure(text="blink", fg=new_color)
            GPIO.output(LED_RED, not GPIO.input(LED_RED))
            self.after(1000, self.blink)


if __name__ == "__main__":
    try:
        root = MyApp()
        root.mainloop()
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()


#EOF