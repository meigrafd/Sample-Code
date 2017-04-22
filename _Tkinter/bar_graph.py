#!/usr/bin/python3
#
#   Creator: meigrafd
#   Copyright (C) 2017 by meiraspi@gmail.com published under the Creative Commons License (BY-NC-SA)
#
# http://www.forum-raspberrypi.de/Thread-python-gui-spannung-als-balken-anzeigen
#
import tkinter as tk


class BarGraph:
    def __init__(self, canvas=None, x=0, y=0, width=20, height=None, color='red', outline='black', title=False, title_align=tk.SW, tags='', value=0):
        self.canvas = canvas
        # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/anchors.html
        self.title_align = title_align
        self.title = title
        self.tags = tags
        # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/coordinates.html
        self.x = x  # Top left to right coordinate
        self.y = y  # Top left to bottom coordinate
        self.background_color = color
        self.border_color = outline
        self.font=('', 6)
        self.width = width
        self.height = height
        self.canvas_width = canvas.winfo_width()
        self.canvas_height = canvas.winfo_height()
        if not self.height:
            self.height = self.canvas_height
        self.set_value(value)
        
        self.y_gap = 5  # Höhe zwischen der unteren linken ecke zum Balken
        self.x_stretch = 2  # Platz zwischen den einzelnen Balken.
        self.x_width = 15  # Breite der Balken
        self.x_gap = 15  # Breite des Abstands des ersten Balken von der unten linken ecke
    
    def set_value(self, value):
        self.value = value
        if self.title is not False and type(self.title) is not str:
            self.title = value
    
    def update(self, value):
        self.canvas.delete(self.bar)
        if self.bar_title:
            self.canvas.delete(self.bar_title)
        self.set_value(value)
        self.draw()
    
    def draw(self):
        # Bottom left coordinate
        if self.x == 0:
            x0 = 0
        else:
            x0 = self.x + self.width
        # Top left coordinates
        y0 = self.height - self.value
        
        # Bottom right coordinates
        x1 = x0 + self.width
        # Top right coordinates
        y1 = self.height
        
        # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_rectangle.html
        # Draw the bar
        self.bar = self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.background_color, outline=self.border_color)
        # Put the title above the bar
        if self.title:
            self.bar_title = self.canvas.create_text(x0 + 3, y0, anchor=self.title_align, font=self.font, text=str(self.title))
        else:
            self.bar_title = None




root = tk.Tk()
root.title("Bar Graph")

c = tk.Canvas(master=root, width=500, height=200)
c.pack()

b1 = BarGraph(canvas=c, color='yellow', value=189)
b1.draw()

b2 = BarGraph(canvas=c, color='blue', x=10, title=True)
b2.set_value(97)
b2.draw()
b2.update(103)

b3 = BarGraph(canvas=c, x=30, value=189, title='bla')
b3.draw()

b3.title=True
b3.update(187)

b3.title='blub'
b3.update(177)

root.mainloop()


# EOF

