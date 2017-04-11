#!/usr/bin/python3
#
# http://www.forum-raspberrypi.de/Thread-python-schleife-beenden-abbrechen?pid=226609#pid226609
#
import tkinter as tk
import RPi.GPIO as GPIO

class GUI:
    def __init__(self, gpiopin=3, debug=False):
        self.gpiopin = gpiopin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(gpiopin, GPIO.OUT)
        self.DEBUG = debug
        self.led_status = False
        self.master = tk.Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.main_menu()
        self.master.mainloop()
    
    def main_menu(self):
        self.master.geometry("450x140+100+100")
        self.master.title("Hauptmenue")
        self.status_label = tk.Label(master=self.master)
        self.status_label.configure(text=" ", fg="red")
        self.status_label.place(x=0, y=0)
        self.led_button = tk.Button(master=self.master, text="LED", command=self.led_menu)
        self.led_button.place(x=10, y=20, height=100, width=100)
        self.exit_button = tk.Button(master=self.master, bg="#229", fg="white", text="Exit", command=self.quit)
        self.exit_button.place(x=340, y=20, height=100, width=100)
    
    def led_menu(self):
        self.led_master = tk.Toplevel()
        self.led_master.geometry("500x170+100+100")
        self.led_master.title("Bewaesserung")
        self.led_exit_button = tk.Button(self.led_master, text="Hauptmenue", fg="red",  command=self.led_master.destroy)
        self.led_exit_button.place(x=400, y=140, height=30, width=100)
        self.led_tgl_button = tk.Button(self.led_master, text="LED Toggle",command=self.led_toggle)
        self.led_tgl_button.place(x=340, y=20, height=100, width=100)
        self.scale1 = tk.Scale(self.led_master, from_=0, to=200, length=200, orient=tk.HORIZONTAL)
        self.scale1.place(x=10, y=20)
        self.set_scale_button = tk.Button(self.led_master, text="Setzen", command=self.start_scale_proceed)
        self.set_scale_button.place(x=10, y=70)
        self.stop_scale_button = tk.Button(self.led_master, text="Stoppen", command=self.stop_scale_proceed)
        self.stop_scale_button.place(x=85, y=70)
    
    def led_toggle(self):
        if self.led_status == False:
            GPIO.output(self.gpiopin, True)
            self.led_status = True
            self.led_tgl_button.config(bg="green",text="Bewaesserung\n laeuft")
        else:
            GPIO.output(self.gpiopin, False)
            self.led_status = False
            self.led_tgl_button.config(bg="red", text="Bewaesserung\n kann\n gestartet\n werden")
    
    def stop_scale_proceed(self):
        self.value = 201
    
    def start_scale_proceed(self):
        self.value = 0
        self.led_automatisch(self.scale1.get())
    
    def led_automatisch(self, scale_value):
        if (self.value < scale_value):
            GPIO.output(self.gpiopin, True)
            self.value += 1
            self.printD(self.value)
            self.led_master.after(1000, self.led_automatisch, scale_value)
        else:
            GPIO.output(self.gpiopin, False)
            self.printD("Done")
    
    def printD(self, text):
        if self.DEBUG:
            print(text)
    
    def quit(self):
        GPIO.cleanup()
        self.master.destroy()
        print("Quit")


if __name__ == '__main__':
    try:
        tkinter_app = GUI(gpiopin=3, debug=True)
    except (KeyboardInterrupt, SystemExit):
        print("Schliesse Programm.")
