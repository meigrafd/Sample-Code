from Tkinter import *

def spinAlpha_KeyRelease(event): 
    print spinAlpha.get()

def spinAlpha_Click(event):
    spinAlpha_KeyRelease(event)
    print spinAlpha.get()

def spinAlpha_cmd():
    print spinAlpha.get()

master = Tk()
master.geometry("50x50")

#Value = IntVar()
#spinAlpha = Spinbox(master, width=4, from_=0, to=255, increment=15, textvariable=Value)

#spinAlpha = Spinbox(master, width=4, from_=0, to=255, increment=15)
spinAlpha = Spinbox(master, width=4, from_=0, to=255, increment=15, command=spinAlpha_cmd)
spinAlpha.bind('<KeyRelease>', spinAlpha_KeyRelease)
spinAlpha.bind('<ButtonRelease-1>', spinAlpha_Click)
spinAlpha.pack()
mainloop()