#!/usr/bin/python3
#
# http://www.forum-raspberrypi.de/Thread-python-bild-als-stream-in-canvas-darstellen?pid=272094#pid272094
#

from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import ImageTk, Image
import tkinter as tk


def main():
    try:
        
        root = tk.Tk()
        
        stream = BytesIO()
        camera = PiCamera()
        camera.start_preview()
        sleep(2)
        camera.capture(stream, format='png', resize=(50, 50))
        stream.seek(0)
        camera.stop_preview()
        
        pic_stream = Image.open(stream, mode='r')
        photo = ImageTk.PhotoImage(pic_stream)
        
        label = tk.Label(root, image=photo)
        label.pack()
        root.mainloop()
    
    except (KeyboardInterrupt, SystemExit):
        print('Quit')
        root.destroy()
    except Exception as error:
        print('Error: ' + str(error))


if __name__ == '__main__':
    main()

#EOF