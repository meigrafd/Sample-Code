#!/usr/bin/python2.7
# ************************************
# ********** Wetterstation ***********
# ************************************
from __future__ import print_function
import pifacedigitalio as pf
import time
import csv
import sys
import statistics
import threading
import Adafruit_DHT
from w1thermsensor import W1ThermSensor  # https://github.com/timofurrer/w1thermsensor
from Tkinter import *

#------------------------------------------------
# Einstellungen
#------------------------------------------------

dht_sensor = Adafruit_DHT.DHT22
gpio = 17 # PIN 11

ds_sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20 , "031591177fff")

logpath = "/media/tauschverzeichnis/"
logFile = "log_ws16.csv"
measurementsFile="ws16_station.csv"
farben = ["White Smoke", "Gainsboro", "red", "orange", "Lime Green", "Purple", "black", "white", "grey", "Dodger Blue", "blue"]            

anzdaten=49

# Variablen für das Auslesen des Logfiles
logdatum=[]
loguhrzeit=[]
logtempa=[]
logtempi=[]
logfeucht=[]
loganzfehler=[]

messtemp_a=[]
messtemp_i=[]
mess_f=[]

#------------------------------------------------
# Funktionen
#------------------------------------------------

def perform_measurement():
    # Innentemperatur und Feuchtigkeit messen
    try:
        # Manchmal kann es zu Fehlmessungen kommen...
        for i in range(1, 100):
            humidity , temperature = Adafruit_DHT.read(dht_sensor , gpio)
            if humidity is not None and temperature is not None:
                break # Wenn Messung Ergebnis liefert, dann for-Schleife unterbrechen
    except:
        print("ACHTUNG: Die Messung der Innentemperatur und der Feuchtigkeit wurde nicht durchgeführt.")
    # Außentemperatur messen
    temperatur_in_celsius = round(ds_sensor.get_temperature(), 1)
    # Ausgaben (Ausgabe nur in Console möglich)
    print("*** Temperaturmessung ***")
    print("")
    print("Datum:            " + time.strftime("%d.%m.%Y"))
    print("Uhrzeit:          " + time.strftime("%H:%M:%S"))
    print("")
    print("Aussentemperatur: " + str(temperatur_in_celsius))
    print("")
    print("Innentemperatur:  %.1f" % temperature)
    print("Luftfeuchtigkeit: %.1f" % humidity)
    print("Anzahl Messungen: " + str(i))
    print("")
    # Messwerte in Datei schreiben
    with open(logpath + measurementsFile, "a") as csvfile:
        # Aufbau Datensatz: Datum; Uhrzeit; Aussentemperatur; Innentemperatur; Feuchtigkeit; Anzahl Messungen
        datensatz = time.strftime("%d.%m.%Y") + "; " + time.strftime("%H:%M:%S") + "; " + "%.1f" % (temperatur_in_celsius)
        datensatz = datensatz + "; " +  str(round(temperature, 1)) + "; " + str(round(humidity)) + "; " + str(i) + "\r\n"
        csvfile.write(datensatz)

# Logdaten lesen
def logeinlesen():
   try:
      with open(logpath + logFile) as csvfile:
         cr = csv.reader(csvfile, delimiter=";")
         for line in cr:
               logdatum.insert(0,line[0])
               loguhrzeit.insert(0,line[1])
               logtempa.insert(0,float(line[2]))
               logtempi.insert(0,float(line[3]))
               logfeucht.insert(0,float(line[4]))
               loganzfehler.insert(0,int(line[5]))
      csvfile.close()
      for i in range(0,len(logdatum)):
         #print(str(i), logdatum[i], loguhrzeit[i], logtempa[i], logtempi[i],logfeucht[i],loganzfehler[i], "\r")
         pass
   except:
      print("Fehler beim Lesen der Datei " + str(logFile))
      messagebox.showinfo("Logfile lesen ", "Die Logdatei " + logFile + " konnte nicht gelesen werden.")


def newThread():
   t = threading.Thread(name='Messung', target=measurement)
   t.start()

# Messung im Hintergrund durchführen
def measurement():
    while True:
        try:
            perform_measurement()
            print("Die Messenung wurde erfolgreich gestartet.")
        except:
            print("Fehler bei der Messung.")
            messagebox.showinfo("Fehler", "Fehler bei der Messung.")
        # Messwerte einlesen
        try:
            with open(measurementsFile) as csvfile:
                cr = csv.reader(csvfile, delimiter=";")
                #messtemp_a=cr.line[0]
                for line in cr:
                    messtemp_a.insert(0,line[2])
                    messtemp_i.insert(0,line[3])
                    mess_f.insert(0,line[4])
            akttempa.config(text=str(messtemp_a[0]))
            akttempi.config(text=str(messtemp_i[0]))
            ergebnis_feuchte=int(float(mess_f[0]))
            aktfeucht.config(text=str(ergebnis_feuchte))
            print("Die Logdatei für die Messung wurde erfogreich gelesen ("+measurementsFile+").")
        except:
            print("Fehler beim Lesen der Logdatei für die Messung innerhalb der Station ("+measurementsFile+").")
            messagebox.showinfo("Fehler Logdatei", "Fehler beim Lesen der Logdatei für Messung innerhalb der Station ("+measurementsFile+").")
        time.sleep(10)


# Löscht das Diagramm
def diagrloeschen():
   w.create_rectangle(0,0,1000,530,fill=farben[7])
 
 
# Diagrammfläche mit horizontalen Achsen erzeugen (ohne Daten aus Logfile)
def diagrerzeug():
 
   w.create_rectangle(200,20,900,420,fill=farben[0],  outline=farben[1], width=2)
   
   #for i in range(1,28):# vertikale Achsen für x Zeitachse
     # w.create_line(i*25+200,20,i*25+200,420, fill=farben[1], width=1)
      
   for i in range(1,20):#horizontale Achsen für Messwerte
      w.create_line(200,20+i*20,900,20+i*20, fill=farben[1], width=1)
      
   # Aussentemperatur
   w.create_line(190,20,190,420,fill=farben[2], width=1)
   w.create_text(100,505, text="Aussentemperatur [°C]",fill=farben[2])
   w.create_text(175,440, text="°C",fill=farben[2])
   tempstart=35
   for i in range(1,12):
      w.create_text(175,i*40-20, text=tempstart,fill=farben[2])
      tempstart-=5
      
   # Innentemperatur
   w.create_line(160,20,160,420,fill=farben[3], width=1)
   w.create_text(260,505, text="Innentemperatur [°C]",fill=farben[3])
   w.create_text(145,440, text="°C",fill=farben[3])
   tempstart=30
   for i in range(1,12):
      w.create_text(145,i*40-20, text=tempstart,fill=farben[3])
      tempstart-=5
 
   # Feuchtigkeit innen
   w.create_line(130,20,130,420,fill=farben[4], width=1)
   w.create_text(400,505, text="Feuchtigkeit [%]",fill=farben[4])
   w.create_text(115,440, text="%",fill=farben[4])
   feuistart=100
   for i in range(1,12):
      w.create_text(115,i*40-20, text=feuistart,fill=farben[4])
      feuistart-=10
 
   # Windgeschwindigkeit
   w.create_line(100,20,100,420,fill=farben[5], width=1)
   w.create_text(530,505, text="Wind [km/h]",fill=farben[5])
   w.create_text(85,440, text="km/h",fill=farben[5])
   windstart=100
   for i in range(1,12):
      w.create_text(83,i*40-20, text=windstart,fill=farben[5])
      windstart-=10
   
   # Niederschlag
   w.create_line(70,20,70,420, fill=farben[10], width=1)
   w.create_text(660,505, text="Niederschlag [l/h]",fill=farben[10])
   w.create_text(53,440, text="l/h",fill=farben[10])
   niederstart=100
   for i in range(1,12):
      w.create_text(53,i*40-20, text=niederstart,fill=farben[10])
      niederstart-=10
 
   # Windrichtung
   w.create_line(40,20,40,420,fill=farben[6], width=1)
   txtwinr=w.create_text(780,505, text="Wind N/S  ",fill=farben[6])   
 
 
# Diagramm mit Logdaten ergänzen
def diagrerstellen():
 
   # Schrittweite berechnen
   if ((schieber2.get())-(schieber1.get()))<=0:
         schrittweite=700# Division durch Null vermeiden
   else:
      schrittweite=700/((schieber2.get())-(schieber1.get()))
 
   # Schieber 1 und 2 beschriften mit Wochentag/Datum/Uhrzeit
   startdatum.config(text=wochentag(logdatum[schieber1.get()-1])+", " +logdatum[schieber1.get()-1])
   startuhrzeit.config(text=loguhrzeit[schieber1.get()-1][:6]+" Uhr")
   enddatum.config(text=wochentag(logdatum[schieber2.get()-1])+", " +logdatum[schieber2.get()-1])
   enduhrzeit.config(text=loguhrzeit[schieber2.get()-1][:6]+" Uhr") 
   
   # Beschriftung der x-Achse und vertikale Hilfslinien einfügen
   y1=440
   zaehler=0
   for i in range(schieber1.get()-1, schieber2.get()):
      xstart=200+round(zaehler*schrittweite,0)
      if xstart<901:
         if y1==430:
            y1=460
         else:
            y1=430
         # Logdatum einfügen
         w.create_text(xstart, y1, text=str(logdatum[i][:6]), fill=farben[8], font=("Arial", 8))
         # Loguhrzeit einfügen
         w.create_text(xstart, y1+10, text=str(loguhrzeit[i][:6]), fill=farben[9], font=("Arial", 8))
         # Linie von Datum zum Diagramm einfügen
         w.create_line(xstart,420,xstart,y1-4,fill=farben[9])
         # vertikale Hilfslinien
         w.create_line(xstart,20,xstart,420, fill=farben[1], width=1)
         zaehler+=1
 
 
   # Startkoordinate für alle Messwerte
   xstart=200
   xende=200
   ystart=0
   yende=0
   
   for i in range(schieber1.get()-1,schieber2.get()-1):
      
      # Aussentemperatur
      xende+=schrittweite
      if logtempa[i]>0:
         ystart=300-round(logtempa[i]*8,0)
         yende=300-round(logtempa[i+1]*8,0)
      else:
         ystart=300+round(logtempa[i]*8*-1,0)
         yende=300+round(logtempa[i+1]*8*-1,0)
      if xende<901:
         w.create_line(xstart,ystart,xende,yende, fill=farben[2], width=3)
         
      # Innentemperatur
      if logtempi[i]>0:
         ystart=300-round(logtempi[i]*8,0)
         yende=300-round(logtempi[i+1]*8,0)
      else:
         ystart=300+round(logtempi[i]*8*-1,0)
         yende=300+round(logtempi[i+1]*8*-1,0)
      if xende<901:
         w.create_line(xstart,ystart,xende,yende, fill=farben[3], width=3)
 
      # Feuchtigkeit
         ystart=420-round(logfeucht[i]*4,0)
         yende=420-round(logfeucht[i+1]*4,0)
      if xende<901:
         w.create_line(xstart,ystart,xende,yende, fill=farben[4], width=3)
 
      xstart+=schrittweite
 
   # Statistik (Mittelwerte rechts neben Diagramm eintragen)
   s1 = schieber1.get()-1
   s2 = schieber2.get()-1
   if (s2-s1)>0:
 
      dstempa=round(statistics.mean(logtempa[s1:s2]),1)
      if dstempa>0:
         ystart=300-round(dstempa*8,0)
      else:
         ystart=300+round(dstempa*8,0)
      w.create_rectangle(910,ystart+8,950,ystart-10, fill=farben[7], outline=farben[2])
      w.create_text(930,ystart,text=str(dstempa), fill=farben[2])
      
 
      dstempi=round(statistics.mean(logtempi[s1:s2]),1)
      if dstempi>0:
         ystart=300-round(dstempi*8,0)
      else:
         ystart=300+round(dstempi*8,0)
      w.create_rectangle(910,ystart+8,950,ystart-10, fill=farben[7], outline=farben[3])
      w.create_text(930,ystart,text=str(dstempi), fill=farben[3])
       
         
      dsfeucht=round(statistics.mean(logfeucht[s1:s2]),0)
      ystart=420-round(dsfeucht*4,0)
      w.create_rectangle(910,ystart+8,950,ystart-10, fill=farben[7], outline=farben[4])
      w.create_text(930,ystart,text=str(int(dsfeucht)), fill=farben[4])
 
# Wochentag ermitteln
def wochentag(datum):
   # Format Datum z.B. "26.06.2016"
   import datetime
   wochentage={0:"Montag", 1:"Dienstag",2:"Mittwoch", 3:"Donnerstag", 4:"Freitag",5:"Samstag", 6:"Sonntag"}
   t=datetime.date(int(datum[6:10]),int(datum[3:5]),int(datum[0:2]))
   return wochentage[t.weekday()]
 

# Aktualisieren
def deffresh():
   if (schieber1.get())>(schieber2.get()):
      # Startzeitpunkt liegt hinter Endzeitpunkt
      messagebox.showinfo("Bereichsauswahl ", "Der Anfangszeitpunkt liegt hinter dem Endzeitpunkt.")
   else:
      # Schieber beschriften mit Datum/Uhrzeit
      startdatum.config(text=logdatum[schieber1.get()-1])
      startuhrzeit.config(text=loguhrzeit[schieber1.get()-1][:6])
      enddatum.config(text=logdatum[schieber2.get()-1])
      enduhrzeit.config(text=loguhrzeit[schieber2.get()-1][:6])     
 
      #logdatum.clear()
      
      logeinlesen()
      diagrloeschen()
      diagrerzeug()
      diagrerstellen()
 
def schieber1set():
   aktwertschieber1=schieber1.get()
   aktwertschieber1=aktwertschieber1+anzdaten-1
   schieber1.set(aktwertschieber1)
    
      
#Aktualisieren +
def deffreshplus():
   schieber2.set(schieber1.get()+schieber3.get()-1)
   deffresh()
 
# Beendet die Wetterstation
def btncklick_be():
   sys.exit()
 
 
#------------------------------------------------
# Hauptprogramm
#------------------------------------------------
 
# Fenster erzeugen
master = Tk()
master.title("Wetterstation WS16")
master.geometry("1120x700")
 
# Zeichenfläche erzeugen
w = Canvas(master,  bg="white")
w.place(x=20,y=20, width=960, height=520)
 
# Button erzeugen
beenden=Button(master, text="Beenden", command=btncklick_be)
beenden.place(x=1000,y=660, width=100, height=30)
 
fresh=Button(master, text="Aktualisieren", command=deffresh)
fresh.place(x=900,y=660, width=100, height=30)
 
freshplus=Button(master, text="Aktualisieren+", command=deffreshplus)
freshplus.place(x=800, y=660, width=100, height=30)
 
freshminus=Button(master, text="Tag -1", command=schieber1set)
freshminus.place(x=700, y=660, width=100, height=30)
 
 
mess=Button(master, text="Messung", command=newThread)
mess.place(x=600,y=660, width=100, height=30)
 
 
 
# logFile einlesen
logeinlesen()
 
# Rahmen mit Text einfügen
zeitrahmen=LabelFrame(master,text="  Betrachtungszeitraum  ")
zeitrahmen.place(x=20,y=550,width=960, height=105)
 
# Schieberegler erzeugen
schieber1 =Scale(zeitrahmen, from_=1, to=len(logdatum), tickinterval=100, orient=HORIZONTAL)
schieber1.set(0)
schieber1.place(x=10, y=0, width=400, height=70)
 
schieber2 =Scale(zeitrahmen, from_=1, to=len(logdatum), tickinterval=100, orient=HORIZONTAL)
schieber2.set(anzdaten)
schieber2.place(x=540, y=0, width=400, height=70)
 
schieber3=Scale(zeitrahmen, from_=1, to=100, orient=HORIZONTAL)
schieber3.place(x=415,y=0, width=120, height=70)
schieber3.set(anzdaten)
 
# Label
startdatum=Label(zeitrahmen, text="", fg=farben[8])
startdatum.place(x=150, y=50)
startuhrzeit=Label(zeitrahmen, text="", fg=farben[9])
startuhrzeit.place(x=190, y=65)
enddatum=Label(zeitrahmen, text="", fg=farben[8])
enddatum.place(x=670, y=50)
enduhrzeit=Label(zeitrahmen, text="", fg=farben[9])
enduhrzeit.place(x=710, y=65)
 
# Rahmen Messung
messrahmen=LabelFrame(master, text=" Akt. Messung ")
messrahmen.place(x=995, y=15, width=105, height=640)
 
akttempa=Label(messrahmen,text="--.-", font=("Arial",24), fg=farben[2])
akttempa.place(x=8,y=5)
beschrtempa=Label(messrahmen, text="Aussentemp.", font=("Arial",8), fg=farben[8])
beschrtempa.place(x=16,y=40)
 
akttempi=Label(messrahmen,text="--.-", font=("Arial",24), fg=farben[3])
akttempi.place(x=8,y=80)
beschrtempi=Label(messrahmen, text="Innentemp.", font=("Arial",8), fg=farben[8])
beschrtempi.place(x=19,y=115)
 
aktfeucht=Label(messrahmen,text="--", font=("Arial",24), fg=farben[4])
aktfeucht.place(x=28,y=150)
beschrfeucht=Label(messrahmen, text="Luftfeuchtigkeit", font=("Arial",8), fg=farben[8])
beschrfeucht.place(x=10,y=185)
 
# Menu
menubar=Menu(master=master)# Menuleiste wird erzeigt
master.config(menu=menubar)# Menuleiste wird ins Fenster eingebaut
menubar.add_command(label="Beenden",command=btncklick_be)# Kommandobutton wird eingebaut
 
funktionen=Menu(master)# Neues Menu eingefügt
menubar.add_cascade(label="Funktionen", menu=funktionen)# Untermenu wird erzeugt
funktionen.add_command(label="Aktualisieren", command=deffresh)# Kommandobutton eingefügt command anpassen
funktionen.add_command(label="Aktualisieren+", command=deffreshplus)
funktionen.add_command(label="Tag-1", command=schieber1set)
funktionen.add_command(label="Messung", command=newThread)
 
 
# Diagramm erzeugen
deffresh()
newThread()
 
master.mainloop()