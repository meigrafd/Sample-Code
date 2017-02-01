from sys import version_info
if version_info[0] < 3:
    import Tkinter as tk
    import tkFont as tkf
else:
    import tkinter as tk
    import tkinter.font as tkf
    
import math

class Meter(tk.Canvas):
    def __init__(self,master,*args,**kwargs):
        tk.Canvas.__init__(self,master,*args,**kwargs)
        self.layoutparams()
        self.graphics()
        self.createhand()
        self.setrange()
        
    def layoutparams(self):
        # set parameters that control the layout
        height = int(self['height'])
        width = int(self['width'])
        
        # find a square that fits in the window
        if(height*2 > width):
            side = width
        else:
            side = height*2
        
        # set axis for hand
        self.centrex = side/2
        self.centrey = side/2
        
        # standard with of lines
        self.linewidth = 2
        
        # outer radius for dial
        self.radius = int(0.40*float(side))
        
        # set width of bezel
        self.bezel = self.radius/15
        self.bezelcolour1 = '#c0c0c0'
        self.bezelcolour2 = '#808080'
    
        # set lengths of ticks and hand
        self.majortick = self.radius/8
        self.minortick = self.majortick/2
        self.handlen = self.radius - self.majortick - self.bezel - 1
        self.blobrad = self.handlen/6
             
    def graphics(self):
        # create the static components
        self.create_oval(self.centrex-self.radius,
        self.centrey-self.radius,
        self.centrex+self.radius,
        self.centrey+self.radius,
        width = self.bezel,
        outline = self.bezelcolour2)
        
        self.create_oval(self.centrex-self.radius - self.bezel,
        self.centrey-self.radius - self.bezel,
        self.centrex+self.radius + self.bezel,
        self.centrey+self.radius + self.bezel,
        width = self.bezel,
        outline = self.bezelcolour1)
        
        for deg in range(-60,241,6):
            self.createtick(deg,self.minortick)
        for deg in range(-60,241,30):
            self.createtick(deg,self.majortick)
        
    def createhand(self):
        # create text display
        self.textid = self.create_text(self.centrex,
        self.centrey - 3*self.blobrad,
        fill = 'red',
        font = tkf.Font(size = -int(2*self.majortick)))
        
        
        # create moving and changeable bits
        self.handid = self.create_line(self.centrex,self.centrey,
        self.centrex - self.handlen,self.centrey,
        width = 2*self.linewidth,
        fill = 'red')
        
        self.blobid = self.create_oval(self.centrex - self.blobrad,
        self.centrey - self.blobrad,
        self.centrex + self.blobrad,
        self.centrey + self.blobrad,
        outline = 'black', fill = 'black')
        
    def createtick(self,angle,length):
        # helper function to create one tick
        rad = math.radians(angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        radius = self.radius - self.bezel
        self.create_line(self.centrex - radius*cos,
        self.centrey - radius*sin,
        self.centrex - (radius - length)*cos,
        self.centrey - (radius - length)*sin,
        width = self.linewidth)
        
    def setrange(self,start = 0, end=100):
        self.start = start
        self.range = end - start
        
    def set(self,value):
        # call this to set the hand
        # convert value to range 0,100
        deg = 300*(value - self.start)/self.range - 240
        
        self.itemconfigure(self.textid,text = str(value))
        rad = math.radians(deg)
        # reposition hand
        self.coords(self.handid,self.centrex,self.centrey,
        self.centrex+self.handlen*math.cos(rad), self.centrey+self.handlen*math.sin(rad))
        
    def blob(self,colour):
        # call this to change the colour of the blob
        self.itemconfigure(self.blobid,fill = colour,outline = colour)



class Meterframe(tk.Frame):
   def __init__(self,master,text = '',scale=(0,100),*args,**kwargs):
      tk.Frame.__init__(self,master,*args,**kwargs)
      
      width = kwargs.get('width',100)
      self.meter = Meter(self,height = width,width = width)
      self.meter.setrange(scale[0],scale[1])
      self.meter.pack()
      
      tk.Label(self,text=text).pack()
      
      tk.Scale(self,length = width,from_ = scale[0], to = scale[1],
      orient = tk.HORIZONTAL,
      command = self.setmeter).pack()
      
   def setmeter(self,value):
      value = int(value)
      self.meter.set(value)
      
class Mainframe(tk.Frame):
   def __init__(self,master,*args,**kwargs):
      tk.Frame.__init__(self,master,*args,**kwargs)
      
      Meterframe(self,text = 'Meter1',width = 200).grid(row = 0,column = 0)
      Meterframe(self,text = 'Meter2',width = 200,scale = (-50,50)).grid(row = 0,column = 1)
            
      tk.Button(self,text = 'Quit',width = 15,command = master.destroy).grid(row = 1,column = 0)

class App(tk.Tk):
   def __init__(self):
      tk.Tk.__init__(self)
      
      self.title('Try Meter')
   
      Mainframe(self).pack()
      
App().mainloop()
