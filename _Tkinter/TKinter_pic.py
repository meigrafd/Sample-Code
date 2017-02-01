try:
	#python3
	import tkinter
except ImportError:
	#python2
	import Tkinter as tkinter
import time
import datetime
import math
import os
import linecache

#----- Variablen
Datum = datetime.datetime.now().strftime("%Y-%m-%d")
#Datei = "/tmp/"+str(Datum)+"_Messdaten.csv"
Datei = "Messdaten.csv"
Bild1 = "/tmp/test/No.gif"
Bild2 = "/tmp/test/Yes.gif"
#-----


# Messdaten.csv:
#
# abc;def;ghi;jkl;mno;pqr;stu;0;yz
#


# Erzeugung des Fensters
tkFenster = tkinter.Tk()
tkFenster.title("ENTEC-E ENTEC7 WS 14/15 - AUTARKES HAUS")
tkFenster.geometry("590x424+-1+-1")

#Bilder
pic1 = tkinter.PhotoImage(file=Bild1)
pic2 = tkinter.PhotoImage(file=Bild2)

#Label Bilder
LabelBilder = tkinter.Label(master=tkFenster, image=pic1)
LabelBilder.place(x=1, y=1)

def readCSV(File, Line):
	lines = linecache.getline(File, Line)
	linecache.clearcache()
	data = lines.strip().split(";")  
	return data

def checkCSV():
	global LabelBilder
	Data = readCSV(Datei, 1)
	print(Data[7])
	if Data[7] == 0:
		LabelBilder.config(image=pic1)
	elif Data[7] == 1:
		LabelBilder.config(image=pic2)
	tkFenster.after(1000, checkCSV)

# Aktivierung des Fensters
try:
	checkCSV()
	tkFenster.mainloop()
except (KeyboardInterrupt, SystemExit):
	print("Schliesse Programm..")