#!/usr/bin/python3
#
# http://www.forum-raspberrypi.de/Thread-raspbian-autostart-nach-x-sekunden-mit-abfrage
#
import tkinter as tk
import shlex
from subprocess import call, Popen

class GUI:
    def __init__(self, cmd="/usr/bin/top", debug=False, startdelay=5):
        self.DEBUG = debug
        self.master = tk.Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.startProgramm = cmd
        self.delay = tk.IntVar()
        self.delay.set(startdelay)
        self.main_menu()
        self.master.mainloop()

    def main_menu(self):
        self.master.geometry("240x200")
        self.master.title("Startverzoegerung")
        self.counter_label = tk.Label(master=self.master)
        self.counter_label.configure(font=("Courier", 30), bg="#229", fg="red", textvariable=self.delay)
        self.counter_label.place(x=100, y=5, height=50, width=50)
        self.exit_button = tk.Button(master=self.master, bg="red", fg="white", text="Exit", command=self.quit)
        self.exit_button.place(x=170, y=130, height=70, width=70)
        self.master.after(2000, self.countdown)

    def countdown(self):
        self.delay.set(self.delay.get() - 1)
        self.printD(self.delay.get())
        if (self.delay.get() < 0):
            self.delay.set(0)
            self.printD("Starte: %s" % self.startProgramm)
            self.master.after(1000, self.start_prog(self.startProgramm))
        else:
            self.master.after(1000, self.countdown)

    def start_prog(self, cmd):
        try:
            #self.process = Popen(shlex.split(cmd))
            self.process = call(cmd, shell=True)
            self.quit()
        except:
            pass

    def printD(self, text):
        if self.DEBUG:
            print(text)

    def quit(self):
        self.master.destroy()
        print("Quit")


if __name__ == '__main__':
    try:
        tkinter_app = GUI(cmd="/path/to/kodi", startdelay=10, debug=True)
    except (KeyboardInterrupt, SystemExit):
        print("Schliesse Programm.")
