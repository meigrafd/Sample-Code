#!/usr/bin/python3
import tkinter as tk
import time
import os.path
import sys
import random



class GUI(object):
    SETTINGS_FILE = "RTIMULib"
    def __init__(self):      
        self.root = tk.Tk()
        self.root.title("test")
        self.root.geometry("800x600")
        self.root.overrideredirect(False)
        
        self.titelLabel = tk.Label(self.root, text = "Messung", relief = "groove")
        self.xLabel = tk.Label(self.root, text = "x-Wert", relief = "groove")
        self.yLabel = tk.Label(self.root, text = "y-Wert", relief = "groove")
        self.zLabel = tk.Label(self.root, text = "z-Wert", relief = "groove")
        
        self.x_Value = tk.IntVar()
        self.y_Value = tk.IntVar()
        self.z_Value = tk.IntVar()
        self.x_Value.set(0)
        self.y_Value.set(0)
        self.z_Value.set(0)
        
        self.x_Color = "red"
        self.y_Color = "green"
        self.z_Color = "blue"
        
        self.xWertLabel = tk.Label(self.root, relief = "groove", textvariable = self.x_Value, foreground = self.x_Color)
        self.yWertLabel = tk.Label(self.root, relief = "groove", textvariable = self.y_Value, foreground = self.y_Color)
        self.zWertLabel = tk.Label(self.root, relief = "groove", textvariable = self.z_Value, foreground = self.z_Color)
        self.X_plotData = []
        self.Y_plotData = []
        self.Z_plotData = []
        
        self.plot_point_color = '#f00'
        self.plot_border_color = '#000'
        self.plot_line_color = '#00f'
        self.plot_background_color = '#fff'
        self.plot_axis_color = '#000'
        self.plotCanvas = tk.Canvas(self.root, background=self.plot_background_color)
        self.plotCanvas.grid(column=1, row=3, columnspan=3, sticky="news")
        self.plot_height = self.plotCanvas.winfo_reqheight()
        self.plot_width = self.plotCanvas.winfo_reqwidth()
        self.setOrigin(0, self.plot_height)
        self.plot_x = 0
        
        self.titelLabel.grid(column=0, row=0, columnspan=5, sticky="news")
        self.xLabel.grid(column=1, row=1, sticky="news")
        self.yLabel.grid(column=2, row=1, sticky="news")
        self.zLabel.grid(column=3, row=1, sticky="news")
        self.xWertLabel.grid(column=1, row=2, sticky="news")
        self.yWertLabel.grid(column=2, row=2, sticky="news")
        self.zWertLabel.grid(column=3, row=2, sticky="news")
        
        self.startbutton = tk.Button(self.root, text="Start", command=self.start)
        self.stoppbutton = tk.Button(self.root, text="Stop", command=self.stopp)
        
        self.startbutton.grid(column=1, row=4, sticky="news")
        self.stoppbutton.grid(column=3, row=4, sticky="news")
        self.startbutton.config(bg="green")
        self.stoppbutton.config(bg="red")
        
        # Size Behavior
        self.root.grid_rowconfigure(0, weight = 1, minsize = 40, pad = 0)
        self.root.grid_rowconfigure(1, weight = 1, minsize = 30, pad = 0)
        self.root.grid_rowconfigure(2, weight = 1, minsize = 30, pad = 0)
        self.root.grid_rowconfigure(3, weight = 1, minsize = 450, pad = 0)
        self.root.grid_rowconfigure(4, weight = 1, minsize = 50, pad = 0)
        
        self.root.grid_columnconfigure(0, weight = 1, minsize = 55, pad = 0)
        self.root.grid_columnconfigure(1, weight = 1, minsize = 230, pad = 0)
        self.root.grid_columnconfigure(2, weight = 1, minsize = 230, pad = 0)
        self.root.grid_columnconfigure(3, weight = 1, minsize = 230, pad = 0)
        self.root.grid_columnconfigure(4, weight = 1, minsize = 55, pad = 0)
    
    def plot(self):
        self.setLineColor(self.x_Color)
        self.addMultipointLine(points = self.X_plotData)
        
        self.setLineColor(self.y_Color)
        self.addMultipointLine(points = self.Y_plotData)
        
        self.setLineColor(self.z_Color)
        self.addMultipointLine(points = self.Z_plotData)
        
        self.root.after(1000, self.plot)

    def start(self):
        self.stop = False
        self.t0 = time.time()
        self.root.after(500, self.Messung)
        self.root.after(2000, self.plot)

    def Messung(self):
        if not self.stop:
            # y = vertical , x = horizontal
            self.x_Value.set( self.x_Value.get() - random.randint(-5, 5) )
            self.y_Value.set( self.y_Value.get() - random.randint(-2, 2) )
            self.z_Value.set( self.z_Value.get() - random.randint(-10, 10) )
            
            self.plot_x = self.getXOrigin() + self.plot_x + 2
            
            self.X_plotData.append( (self.plot_x, self.getYOrigin() + self.x_Value.get()) )
            self.Y_plotData.append( (self.plot_x, self.getYOrigin() + self.y_Value.get()) )
            self.Z_plotData.append( (self.plot_x, self.getYOrigin() + self.z_Value.get()) )

            self.root.after(500, self.Messung)
    
    def stopp(self):
        self.stop = True
        print("gestoppt")
    
    def run(self):
        self.root.mainloop()
    
    def addPoint(self, x, y, txtVal):
        self.plotCanvas.create_line(x+1, y-1, x-1, y+1, tags='all', fill=self.plot_point_color)
        self.plotCanvas.create_text(x+50, y, font=("Comic Sans MS",8), text=txtVal, fill=self.plot_axis_color)
    
    def addLine(self, x0, y0, x1, y1):
        self.plotCanvas.create_line(x0, y0, x1, y1, tags='all', fill=self.plot_line_color)
    
    def addMultipointLine(self, points):
        self.plotCanvas.create_line(arrow=tk.LAST, arrowshape=(4,4,0), tags='all', fill=self.plot_line_color, *points)
    
    def setPointColor(self, color):
        self.plot_point_color = color
    
    def setAxisColor(self, color):
        self.plot_axis_color = color
    
    def setBorderColor(self, color):
        self.plot_border_color = color
    
    def setBackgroundColor(self, color):
        self.plot_background_color = color
    
    def setLineColor(self, color):
        self.plot_line_color = color
    
    def clear(self):
        self.plotCanvas.delete('all')
    
    def setOrigin(self, x, y):
        self.plot_xOrigin = x
        self.plot_yOrigin = y
    
    def getXOrigin(self):
        return self.plot_xOrigin
    
    def getYOrigin(self):
        return self.plot_yOrigin
    


p = GUI().run()

#EOF
