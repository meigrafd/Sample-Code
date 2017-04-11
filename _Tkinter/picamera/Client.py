#!/usr/bin/python3
#
# Copyright (C) 2017 by meiraspi@gmail.com published under the MIT License
#
# Socket Client to stream raspicam in tkinter
#

import socket
import struct
import pickle
import tkinter as tk
from sys import exit, stdout
from time import sleep, strftime
from PIL import Image, ImageTk
from threading import Thread


DEBUG=False


def printD(message):
    if DEBUG:
        print('[{}]  {}'.format(strftime('%H:%M:%S'), message))
        stdout.flush()


class streamClient(object):
    def __init__(self, gui, host='127.0.0.1', port=8000):
        self.gui = gui
        self.host = host
        self.port = port
        self.running = False
    
    def start(self):
        self.client_socket = socket.socket()
        self.client_socket.settimeout(10)
        try:
            self.client_socket.connect((self.host, self.port))
        except (socket.timeout, ConnectionRefusedError) as Error:
            print(Error)
            self.stop()
            return
        self.client_socket.settimeout(None)
        # Make a file-like object out of the connection
        self.connection = self.client_socket.makefile('rb')
        self.running = True
        
        self.t = Thread(target=self.update, args=())
        self.t.setDaemon(1)
        self.t.start()
        #self.gui.master.after(70, self.update_2)
        
        sleep(0.2) #give videostream some time to start befor frames can be read
    
    def update(self):
        while self.running:
            # Read the length of the image as a 32-bit unsigned int.
            data_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
            if data_len:
                printD('Updating...')
                printD('data_len: %s' % data_len)
                data = self.connection.read(data_len)
                deserialized_data = pickle.loads(data)
                printD('Frame received')
                #print(deserialized_data)
                img = Image.fromarray(deserialized_data)
                newImage = ImageTk.PhotoImage(img)
                self.gui.stream_label.configure(image=newImage)
                self.gui.stream_label.image = newImage
                printD("image updated")
            else:
                time.sleep(0.1)
    
    def update_2(self):
        if self.running == False:
            return
        # Read the length of the image as a 32-bit unsigned int.
        data_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
        if data_len:
            printD('Updating...')
            printD('data_len: %s' % data_len)
            data = self.connection.read(data_len)
            deserialized_data = pickle.loads(data)
            printD('Frame received')
            #print(deserialized_data)
            stdout.flush()
            img = Image.fromarray(deserialized_data)
            newImage = ImageTk.PhotoImage(img)
            self.master.stream_label.configure(image=newImage)
            self.master.stream_label.image = newImage
        self.gui.master.after(70, self.update_2)
    
    def quit(self):
        try: self.stop()
        except: pass
    
    def stop(self):
        # indicate that the thread should be stopped
        self.running = False
        try: self.connection.close()
        except: pass
        try: self.client_socket.close()
        except: pass
        self.client_socket = None


class GUI(object):
    def __init__(self, resolution="640x480", stream_resolution=(320, 240), host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.gui_resolution = resolution
        self.stream_resolution = stream_resolution
        self.running = False
        self.master = tk.Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.main()
    
    def main(self):
        self.videostream = streamClient(gui=self, host=self.host, port=self.port)
        self.master.geometry(self.gui_resolution)
        self.master.title("picamera network stream to tkinter")
        self.startstop_button = tk.Button(master=self.master, text="Start", bg="green", command=self.startstop_stream)
        self.startstop_button.place(x=10, y=10, height=50, width=50)
        self.stream_label = tk.Label(master=self.master)
        self.stream_label.place(x=60, y=10)
        self.exit_button = tk.Button(master=self.master, bg="#229", fg="white", text="Exit", command=self.quit)
        self.exit_button.place(x=10, y=200, height=50, width=50)
    
    def startstop_stream(self):
        # start
        if self.running == False:
            printD("Start")
            self.startstop_button.config(bg="red", text="Stop")
            self.running = True
            self.videostream.start()
        # stop
        else:
            printD("Stop")
            self.startstop_button.config(bg="green", text="Start")
            self.running = False
            self.videostream.stop()
    
    def run(self):
        self.master.mainloop()
    
    def quit(self):
        self.running = False
        self.videostream.quit()
        self.master.destroy()
        print('\nQuit\n')


def main(DEBUG=True):
    screen_width  = 400
    screen_height = 300
    stream_resolution = (320, 240)
    
    try:
        tkinter_app = GUI(host='192.168.0.12', port=8000, resolution="{0}x{1}".format(screen_width, screen_height), stream_resolution=stream_resolution)
        tkinter_app.run()
    except (KeyboardInterrupt, SystemExit):
        print('\nQuit\n')
        tkinter_app.quit()
    except Exception as error:
        print('Error: ' + str(error))
        exit()


if __name__ == '__main__':
    main()


#EOF
