#!/usr/bin/python3
#
#   Creator: meigrafd
#   Copyright (C) 2017 by meiraspi@gmail.com published under the Creative Commons License (BY-NC-SA)
#
# http://www.forum-raspberrypi.de/Thread-python-gui-spannung-als-balken-anzeigen
# http://www.forum-raspberrypi.de/Thread-python-re-gui-spannung-als-balken-anzeigen
#
import tkinter as tk


class BarGraph(object):
    def __init__(self, canvas, x=0, y=0, width=20, height=None, color='red',
                 outline='black', title=False, title_align=tk.SW, tags='',
                 value=0):
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
        self.font = ('', 6)
        self.width = width
        self.height = height
        self.canvas_width = canvas.winfo_width()
        self.canvas_height = canvas.winfo_height()
        if self.height is None:
            self.height = self.canvas_height
        self.bar, self.bar_title = None, None
        self.value = value

        self.set_value(value)

    def set_value(self, value):
        self.value = value
        if self.title and not isinstance(self.title, str):
            self.title = value

    def update(self, value):
        if self.bar is not None:
            self.canvas.delete(self.bar)
        if self.bar_title is not None:
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
        self.bar = self.canvas.create_rectangle(
            x0, y0, x1, y1, fill=self.background_color,
            outline=self.border_color)
        
        # Put the title above the bar
        if self.title:
            self.bar_title = self.canvas.create_text(
                x0 + 3, y0, anchor=self.title_align, font=self.font,
                text=str(self.title))



### Sample:

root = tk.Tk()
root.title("Bar Graph / Chart Bar")
root.geometry("600x300")

mainFrame = tk.Frame(root, relief=tk.SUNKEN, width=550, height=300)
mainFrame.pack()

c = tk.Canvas(master=mainFrame, width=500, height=250)
c.pack()
mainFrame.update()

b1 = BarGraph(canvas=c, color='yellow', value=189)
b1.draw()

b2 = BarGraph(canvas=c, color='blue', x=10, title=True)
b2.set_value(97)
b2.draw()
b2.update(113)

b3 = BarGraph(canvas=c, x=30, value=189, title='bla')
b3.draw()

b3.title='blub'
b3.update(157)

b4 = BarGraph(canvas=c, x=60, value=22, title=True)
b4.draw()

def update_scale_bar(event):
    value = scale1.get()
    b4.update(value)

scale1 = tk.Scale(root, from_=0, to=200, length=200, orient=tk.HORIZONTAL)
scale1.bind("<ButtonRelease-1>", update_scale_bar)
scale1.place(x=150, y=20)

root.mainloop()


# EOF

