#!/usr/bin/python3
# coding: utf-8
from tkinter import *

BGCOLOR="#229"

def Hochzaehlen(event=None):
    sollwert.set(sollwert.get() + 1)

def Runterzaehlen(event=None):
    sollwert.set(sollwert.get() - 1)

def Bestaetigen():
    bestaetigen = "Eingestellter Sollwert " + str(sollwert.get())
    confirm_label.config(text=bestaetigen)
    confirmed.set(True)

def Starten():
    if confirmed.get() == True:
        read_sensor_data(istwert_label)


def read_sensor_data(label):
    istwert.set(istwert.get() + 1)
    if istwert.get() == sollwert.get():
        confirmed.set(False)
        istwert.set(0)
    else:
        label.after(1000, read_sensor_data, label)


# Main Window: Fullscreen
window = Tk()
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
window.geometry(str(w) +"x"+ str(h) +"+0+0")
window.configure(background=BGCOLOR)
#window["bg"] = BGCOLOR

istwert = IntVar()
sollwert = IntVar()
confirmed = BooleanVar()
confirmed.set(False)

solltext_label = Label(master=window, bg=BGCOLOR, font=("Courier", 25), fg="white", text="Sollwert")
sollwert_label = Label(master=window, bg=BGCOLOR, font=("Courier", 25), fg="white", textvariable=sollwert)
isttext_label  = Label(master=window, bg=BGCOLOR, font=("Courier", 25), fg="white", text="Istwert")
istwert_label  = Label(master=window, bg=BGCOLOR, font=("Courier", 25), fg="white", textvariable=istwert)
confirm_label  = Label(master=window, bg=BGCOLOR, font=("Courier", 25), fg="white", text="Eingestellter Sollwert 0")

up_button      = Button(master=window, bg=BGCOLOR, fg="white", text="Hochzaehlen", command=Hochzaehlen)
down_button    = Button(master=window, bg=BGCOLOR, fg="white", text="Runterzaehlen", command=Runterzaehlen)
confirm_button = Button(master=window, bg=BGCOLOR, fg="white", text="Bestaetigen", command=Bestaetigen)
start_button   = Button(master=window, bg=BGCOLOR, fg="white", text="Start", command=Starten)
exit_button    = Button(master=window, bg=BGCOLOR, fg="white", text="X", command=window.destroy)

solltext_label.grid(row=0, column=0)
sollwert_label.grid(row=0, column=1)

up_button.grid(row=0, column=2)
down_button.grid(row=0, column=3)
confirm_button.grid(row=0, column=4)
start_button.grid(row=0, column=5)

confirm_label.grid(row=1, column=2)

isttext_label.grid(row=2, column=0)
istwert_label.grid(row=2, column=1)

exit_button.grid(row=4, column=5)

window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(1, weight=1)


window.mainloop()