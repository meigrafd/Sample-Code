from tkinter import *
import tkinter as tk
import time
import os.path
import sys
import random


class GraphException(Exception):
    def __init__(self, string):
        Exception.__init__(self, string)
      
class Graph(Canvas):
    def __init__(self, master, **options):
        Canvas.__init__(self, master, **options)
        self.width = None
        self.height = None
        self.points = []
        self.lines = []
        self.axes = []
        self.border = None
        self.axis_color = '#000'
        self.point_color = '#f00'
        self.border_color = '#000'
        self.line_color = '#00f'
        self.background_color = '#fff'
      
    def addAxes(self, xmin, xmax, ymin, ymax):
        self.border = self.create_rectangle(xmin, -ymin, xmax, -ymax, tags='all', outline=self.border_color, fill=self.background_color)
        self.axes.append(self.create_line(xmin, 0, xmax, 0, tags='all', fill=self.axis_color))
        self.axes.append(self.create_line(0, -ymin, 0, -ymax, tags='all', fill=self.axis_color))
      
    def addPoint(self, x, y, txtVal):
        self.create_line(x+1, y-1, x-1, y+1, tags='all', fill=self.point_color)
        self.create_text(x+50,y, font=("Comic Sans MS",8), text=txtVal, fill=self.axis_color)
        
    def addLine(self, x0, y0, x1, y1):
        self.create_line(x0, y0, x1, y1, tags='all', fill=self.line_color)
    
    def addMultipointLine(self, points):
        self.create_line(arrow=LAST, arrowshape=(4,4,0), tags='all', fill=self.line_color, *points)
      
    def setPointColor(self, color):
        self.point_color = color
      
    def setAxisColor(self, color):
        self.axis_color = color
      
    def setBorderColor(self, color):
        self.border_color = color
      
    def setBackgroundColor(self, color):
        self.background_color = color
      
    def setLineColor(self, color):
        self.line_color = color
      
    def saveToEPSFile(self, filename):
        self.postscript(colormode='color', file=filename)
      
    def clear(self):
        self.delete('all')
    
    def setOrigin(self, x, y):
        self.xOrigin = x
        self.yOrigin = y
    
    def getXOrigin(self):
        return self.xOrigin
    
    def getYOrigin(self):
        return self.yOrigin
    
    def setAxisLabel(self, x, y):
        self.xSteps = x
        self.ySteps = y
        
    def drawAxisLabel(self):
        #add axis lables
        y = self.yOrigin
        while y > 0 :
            strY = str(self.yOrigin-y)
            self.create_text(self.xOrigin, y, text=strY, fill=self.axis_color)
            y -= self.ySteps
        x = self.width - self.xSteps
        while x > self.xOrigin :
            strX = str(x)
            self.create_text(x, self.yOrigin, text=strX, fill=self.axis_color)
            x -= self.xSteps


class GUI(object):
    SETTINGS_FILE = "RTIMULib"
    def __init__(self):      
        self.root = tk.Tk()
        self.root.title("test")
        self.root.geometry("800x600")
        self.root.overrideredirect(False)
        
        self.titelLabel = tk.Label(self.root, text="Messung", relief = "groove")
        self.xLabel = tk.Label(self.root, text ="x-Wert", relief = "groove")
        self.yLabel = tk.Label(self.root, text ="y-Wert", relief = "groove")
        self.zLabel = tk.Label(self.root, text ="z-Wert", relief = "groove")
        
        self.x_Value = tk.StringVar()
        self.y_Value = tk.StringVar()
        self.z_Value = tk.StringVar()
        self.xWertLabel = tk.Label(self.root, relief = "groove", textvariable = self.x_Value)
        self.yWertLabel = tk.Label(self.root, relief = "groove", textvariable = self.y_Value)
        self.zWertLabel = tk.Label(self.root, relief = "groove", textvariable = self.z_Value)
        
        self.plotCanvas = tk.Canvas(self.root, background='white')
        self.plotCanvas.grid(column=1, row=3, columnspan=3, sticky="news")
        self.plot_width = self.plotCanvas.winfo_reqwidth()
        self.plot_height = self.plotCanvas.winfo_reqheight()
        self.plot_point_color = '#f00'
        self.plot_border_color = '#000'
        self.plot_line_color = '#00f'
        self.plot_background_color = '#fff'
        self.plot_axis_color = '#000'
        
        self.plotData = []
        
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
        #self.plotCanvas.create_line(self.plotData, fill='black')
        #self.plotCanvas.update()
        self.addMultipointLine(points=self.plotData)
    
    def start(self):
        self.stop = False
        self.t0 = time.time()
        self.root.after(500, self.Messung)
        self.root.after(2000, self.plot)
    
    def Messung(self):
        if not self.stop:
            X = round(random.uniform(0.0, 99.0), 6)
            Y = round(random.uniform(0.0, 99.0), 6)
            Z = round(random.uniform(0.0, 99.0), 6)
            self.x_Value.set(X)
            self.y_Value.set(Y)
            self.z_Value.set(Z)
            
            self.plotData.append( (self.getXOrigin() + X, self.getYOrigin() + Y) )
            
            #self.plotData.append((X, Y))
            
            #self.addLine( self.getXOrigin(), self.getYOrigin(), X, Y )
            
            self.root.after(100, self.Messung)
    
    def stopp(self):
        self.stop = True
        print("gestoppt")
    
    def run(self):
        self.root.mainloop()
    
    def scaleAndCenter(self):
        # Find the scale factor from size of bounding box
        bb = self.plotCanvas.bbox('all')
        bbwidth = int(bb[2]) - int(bb[0])
        bbheight = int(bb[3]) - int(bb[1])
        xscale = self.plot_width / bbwidth
        yscale = self.plot_height / bbheight
        # Scale accordingly
        self.plotCanvas.scale('all', 0, 0, xscale, yscale)
        # Move to center the image on the canvas
        bb = self.plotCanvas.bbox('all')
        bbwidth = int(bb[2]) - int(bb[0])
        bbheight = int(bb[3]) - int(bb[1])
        self.plotCanvas.move('all', self.plot_width/2 - bbwidth/2, self.plot_height/2 + bbheight/2)
      
    def addPoint(self, x, y, txtVal):
        self.plotCanvas.create_line(x+1, y-1, x-1, y+1, tags='all', fill=self.plot_point_color)
        self.plotCanvas.create_text(x+50, y, font=("Comic Sans MS",8), text=txtVal, fill=self.plot_axis_color)
        
    def addLine(self, x0, y0, x1, y1):
        self.plotCanvas.create_line(x0, y0, x1, y1, tags='all', fill=self.plot_line_color)
    
    def addMultipointLine(self, points):
        self.plotCanvas.create_line(arrow=LAST, arrowshape=(4,4,0), tags='all', fill=self.plot_line_color, *points)
      
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
      
    def saveToEPSFile(self, filename):
        self.plotCanvas.postscript(colormode='color', file=filename)
      
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