#!/usr/bin/python3
#
# https://gist.github.com/trousers2000/df535ae365779d3281d3b895c5e30548
#
from tkinter import *
 	 
class GraphException(Exception):
	def __init__(self, string):
		Exception.__init__(self, string)
 	 
class Graph(Canvas):
	def __init__(self, master, **options):
		Canvas.__init__(self, master, **options)
		if 'width' in options and 'height' in options:
			self.width = int(options['width'])
			self.height = int(options['height'])
		else:
			raise GraphException('Must specify a height and width.')
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
		self.border = self.create_rectangle(xmin, -ymin, xmax, -ymax, tags='all',outline=self.border_color,fill=self.background_color)
		self.axes.append(self.create_line(xmin, 0, xmax, 0, tags='all',fill=self.axis_color))
		self.axes.append(self.create_line(0, -ymin, 0, -ymax, tags='all',fill=self.axis_color))
 	 
	def scaleAndCenter(self):
 	 # Find the scale factor from size of bounding box
		bb = self.bbox('all')
		bbwidth = int(bb[2]) - int(bb[0])
		bbheight = int(bb[3]) - int(bb[1])
		xscale = self.width / bbwidth
		yscale = self.height / bbheight
 	 # Scale accordingly
		self.scale('all', 0, 0, xscale, yscale)
 	 # Move to center the image on the canvas
		bb = self.bbox('all')
		bbwidth = int(bb[2]) - int(bb[0])
		bbheight = int(bb[3]) - int(bb[1])
		self.move('all', self.width/2 - bbwidth/2, self.height/2 + bbheight/2)
 	 
	def addPoint(self, x, y, txtVal):
		self.create_line(x+1, y-1, x-1, y+1, tags='all', fill=self.point_color)
		self.create_text(x+50,y, font=("Comic Sans MS",8), text=txtVal,fill=self.axis_color)
		
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
	
	def setAxisLabel(self,x,y):
		self.xSteps = x
		self.ySteps = y
		
	def drawAxisLabel(self):
		#add axis lables
		y=self.yOrigin
		while y > 0 :
			strY = str(self.yOrigin-y)
			self.create_text(self.xOrigin,y,text=strY,fill=self.axis_color)
			y-= self.ySteps
		x = self.width -self.xSteps
		while x > self.xOrigin :
			strX = str(x)
			self.create_text(x,self.yOrigin,text=strX,fill=self.axis_color)
			x-=self.xSteps
	
	

window = Tk()
#code here to specify graph size
graph = Graph(window,height=325,width=450)

#specify location of origin
y = 300
x = 25
graph.setOrigin(x,y)

#draws white box within canvas
graph.addAxes(0,100,0,250)
graph.scaleAndCenter() 

#plot a point
graph.setPointColor("red")
#enter x and y values against scale on graph
xValue = 200
yValue =150
textVal = "Some Data (%s,%s)"%(xValue,yValue)
xLocation = graph.getXOrigin() + xValue
yLocation = graph.getYOrigin() - yValue
#graph.addPoint(xLocation, yLocation, textVal)

#Draw a line
xValue = 200
yValue =150
xLocation = graph.getXOrigin() + xValue
yLocation = graph.getYOrigin() - yValue
graph.setLineColor("red")
#graph.addLine(graph.getXOrigin(),graph.getYOrigin(),xLocation,yLocation)

#draw mulitpoint line
xylist=[graph.getXOrigin() + 50,graph.getYOrigin() - 25, graph.getXOrigin() + 100, graph.getYOrigin() - 25, graph.getXOrigin() + 150, graph.getYOrigin() - 130 ]
graph.addMultipointLine(points=xylist)

#specify distance between axis lables
ySteps = 50
xSteps = 50
graph.setAxisLabel(xSteps,ySteps)
#draw axis lables
graph.drawAxisLabel()
 
graph.pack()
window.mainloop()