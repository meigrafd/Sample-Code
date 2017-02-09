#!/usr/bin/python2
#
# http://www.forum-raspberrypi.de/Thread-python-aktualisierung-von-unbestimmten-labels
#
# 08.02.2017  Copyright (C) by meigrafd (meiraspi@gmail.com) published under the MIT License
#
import Tkinter as tk



class App(object):
    def __init__(self, MaschinenDatei=None):
        self.MaschinenDatei = MaschinenDatei
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
    
    
    def run(self):
        container = tk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames={}
        for F in (MainPage, Abteilung):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("MainPage")
        self.root.mainloop()
    
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    
    
    def quit(self):
        self.root.destroy()
        print "Quit"


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.B_Beenden = tk.Button(self, text="Beenden", fg="Black", command=controller.quit)
        self.B_Beenden.grid(column=3, row = 0)
        self.B_Abteilung = tk.Button(self, text="Abteilung", command=lambda:controller.show_frame("Abteilung"))
        self.B_Abteilung.grid(column=0, row = 0)


class Abteilung(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        
        self.B_Beenden = tk.Button(self, text="Beenden", fg="Black", command=controller.quit)
        self.B_Beenden.grid(column=1, row = 0)
        self.B_zurueck = tk.Button(self, text="Zurueck", fg="Black", command=lambda:controller.show_frame("MainPage"))
        self.B_zurueck.grid(column=0, row = 0)
        
        self.createLabels()
        self.running = True
        self.parent.after(1000, self.updateLabelColors)
    
    
    def Maschinenanzahl(self, Datei):
        with open(Datei, 'rb') as f:
            return len(f.readlines())
    
    
    def getColor(self, Datei):
        with open(Datei, "r") as f:
            letztezeile = (list(f)[-1]).rstrip('\n')
            if letztezeile.find("gruen") > 0:
                return "green"
            elif letztezeile.find("Gelb") > 0:
                return "yellow"
            elif letztezeile.find("rot")> 0:
                return "red"
        return "gray"
    
    
    def updateLabelColors(self):
        for num in self.machine_status_labels:
            self.MachineColor[num] = self.getColor(self.MachineFile[num])
            self.machine_status_labels[num].configure(bg=self.MachineColor[num])
        if self.running:
            self.parent.after(1000, self.updateLabelColors)
    
    
    def createLabels(self):
        self.machine_labels=dict()
        self.machine_status_labels=dict()
        self.MachineName=dict()
        self.MachineFile=dict()
        self.MachineColor=dict()
        
        self.Machines = self.Maschinenanzahl(self.controller.MaschinenDatei)
        n=1; i=1
        while i < self.Machines:
            with open(self.controller.MaschinenDatei, "r") as f:
                lines = f.readlines()
                self.MachineName[n] = str(lines[i-1]).rstrip('\n')
                self.MachineFile[n] = str(lines[i]).rstrip('\n')
                self.MachineColor[n] = self.getColor(self.MachineFile[n])
                n+=1; i+=2
        
        for num in self.MachineName:
            self.machine_labels[num] = tk.Label(self, text=self.MachineName[num])
            self.machine_labels[num].grid(row=1 * num, column=0)
            
            self.machine_status_labels[num] = tk.Label(self, text="Ist-Stand", bg=self.MachineColor[num])
            self.machine_status_labels[num].grid(row=num * i, column=1)


if __name__ == "__main__":
    try:
        GUI = App(MaschinenDatei="/tmp/test").run()
    except (KeyboardInterrupt, SystemExit):
        try: GUI.quit()
        except: pass


#EOF