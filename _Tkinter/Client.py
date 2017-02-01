import socket
from Tkinter import *
import threading

Ziel = "127.0.0.1"
Port = 5000

HF = Tk()
HF.title("Steuerung")
HF.geometry("400x500")

def TimedRequest(when, what):
  global timed
  when = float(when)
  what = str(what)
  if not conn:
    Verbinden()
  conn.sendall( what + "\n" )
  received = conn.recv(4096)
  Text1.configure(state=NORMAL)
  Text1.insert(END, (received))
  Text1.configure(state=DISABLED)
  timed = threading.Timer( when, TimedRequest, [when, what] )
  timed.start() 

def Verbinden():  
  global conn, timed
  conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    conn.connect((Ziel, Port))
    Status.configure(text="Verbunden", fg="green") 
    timed = threading.Timer( 2.0, TimedRequest, ["2.0", "pitemp"] )
    timed.start() 
  except:
    Status.configure(text="Failed", fg="red")
    timed.cancel()

def Trennen():
  conn.close()
  timed.cancel()
  Status.configure(text="Getrennt", fg="red")
  Text1.configure(state=NORMAL)
  Text1.delete("1.0", END)
  Text1.configure(state=DISABLED)

def Senden():
  conn.sendall( e1.get() + "\n" )
  received = conn.recv(4096)
  Text1.configure(state=NORMAL)
  Text1.insert(END, (received))
  Text1.configure(state=DISABLED)

Status = Label(HF)
Status.configure(text="Getrennt", fg="red")
Status.grid(row=0, column=2)
e1 = Entry(HF, width=20)
e1.grid(row=1, column=4)
but1 = Button(HF, text="Verbinden", width=10, command=Verbinden)
but1.grid(row=1, column=1)
but2 = Button(HF, text="Trennen", width=10, command=Trennen)
but2.grid(row=1, column=2)
but3 = Button(HF, text="Senden", width=10, command=Senden)
but3.grid(row=1, column=3)

Text1=Text(HF, height=22, width=25)
Text1.configure(state=DISABLED)
Text1.grid(row=2, column=1, columnspan=3)

try:
  mainloop()
except (KeyboardInterrupt, SystemExit):
  print("Schliesse Programme..")
  timed.cancel()
except:
  timed.cancel()