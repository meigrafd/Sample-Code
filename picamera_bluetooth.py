#!/usr/bin/python3
from bluetooth import *
from picamera import *
import sys
import time
import io

addr = "08:37:3D:E9:A9:42"
uuid = "8c25be10-10bb-11e4-9191-0800200c9a66"

print("Suche Server...")
service = find_service(uuid = uuid, address = addr)
if len(service) == 0 :
    print("Kein Server gefunden.")
    sys.exit(0)

server_info = service[0]
port = server_info["port"]
host = server_info["host"]
name = server_info["name"]

print("Verbinden mit Server...")

server_sock = BluetoothSocket(RFCOMM)
server_sock.connect((host,port))

print("Verbunden.")


class Streamer:
    def __init__(self, socket):
        self.socket = socket
        
    def write(self, data):
        data_size = len(data)
        size_buffer = [(data_size >> i & 0xff) for i in (24,16,8,0)]
        self.socket.sendall(buffer(bytearray(x for x in size_buffer),0,4))
        self.socket.sendall(data)

camera = PiCamera()

stream = Streamer(server_sock)
camera.vflip = True
camera.resolution = (200,150)
while True : 
    camera.capture(stream,format="jpeg",use_video_port=True)
    time.sleep(0.01)
print("Verbingung beenden...")
server_sock.close()
print("Beendet.")