#!/usr/bin/python3
#
# Copyright (C) 2017 by meiraspi@gmail.com published under the MIT License
#
# Socket Server awaiting connection to stream raspicam
#
# http://www.forum-raspberrypi.de/Thread-python-problem-tkinter-socket-client-for-raspicam-live-stream
#

import socket
import struct
import msgpack
import msgpack_numpy
import picamera
from sys import stdout
from time import sleep, strftime
from picamera.array import PiRGBArray
from threading import Thread


DEBUG=False


def printD(message):
    if DEBUG:
        print('[{}]  {}'.format(strftime('%H:%M:%S'), message))
        stdout.flush()


class PiVideoStream(object):
    def __init__(self, resolution=(320, 240), format='rgb', framerate=24, led=True):
        self.camera_led = led
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True)
        self.frame = None
        self.running = False
        #dirty but currently the only way so it works immediately
        self.start()
        self.stop()
    
    def start(self):
        printD("videostream: start")
        # start the thread to read frames from the video stream
        if self.camera_led:
            self.camera.led = self.camera_led
        self.running = True
        Thread(target=self.update, args=()).start()
        sleep(0.2) #give videostream some time to start befor frames can be read
    
    def stop(self):
        printD("videostream: stop")
        # indicate that the thread should be stopped
        self.camera.led = False
        self.running = False
    
    def update(self):
        # keep looping infinitely until the thread is stopped
        for frameBuf in self.stream:
            # grab the frame from the stream and clear the stream in preparation for the next frame
            self.frame = frameBuf.array
            self.rawCapture.truncate(0)
            # if the thread indicator variable is set, stop the thread
            if self.running == False:
                return
    
    def read(self):
        # return the frame most recently read
        return self.frame
    
    def quit(self):
        # resource camera resources
        try:
            self.running = False
            self.stream.close()
            self.rawCapture.close()
            self.camera.close()
        except:
            pass



class streamServer(object):
    def __init__(self, videostream=None, host='0.0.0.0', port=8000):
        self.videostream = videostream
        self.host = host
        self.port = port
        self.running = False
        self.start_socket()
        
    def start_socket(self):
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        #self.server_socket.setblocking(1)
    
    def start(self):
        printD("streamserver: start")
        self.running = True
        while self.running:
            frame = self.videostream.read()
            serialized_data = msgpack.packb(frame, default=msgpack_numpy.encode)
            # Write the length of the capture to the stream and flush to ensure it actually gets sent
            data_len = len(serialized_data)
            printD("data_len: %d" % data_len)
            self.connection.write(struct.pack('<L', data_len))
            self.connection.flush()
            # Send the image data over the wire
            self.connection.write(serialized_data)
            self.connection.flush()
            printD("send.")
            sleep(0.001)
    
    def stop(self):
        printD("streamserver: start")
        # indicate that the thread should be stopped
        self.running = False
    
    def quit(self):
        # resource resources
        try:
            self.running = False
            self.videostream.quit()
            try: self.client.close()
            except: pass
            try: self.server_socket.close()
            except: pass
            self.client = None
            self.server_socket = None
        except:
            pass
    
    def run(self):
        while True:
            print("Waiting for Connection...")
            self.client, self.client_addr = self.server_socket.accept()
            if self.client:
                self.connection = self.client.makefile('wb')
            print("Connected: %s" % self.client_addr[0])
            try:
                self.videostream.start()
                self.start()
            except: pass
            finally:
                print("Disconnected")
                self.stop()
                try: self.videostream.stop()
                except: pass
                try: self.client.close()
                except: pass
                try: self.connection.close()
                except: pass


if __name__ == '__main__':
    stream_resolution = (320, 240)
    stream_framerate = 15
    picamera_led = True
    
    try:
        vs = PiVideoStream(resolution=stream_resolution, framerate=stream_framerate, led=picamera_led)
        stream = streamServer(videostream=vs).run()
    except (KeyboardInterrupt, SystemExit):
        try: stream.quit()
        except: pass
        print('\nQuit\n')


#EOF
