#!/usr/bin/python3
#
# http://www.forum-raspberrypi.de/Thread-kamera-modul-unterbrechungsfreier-streamer-fuer-picamera?pid=203406#pid203406
#
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import io
import os
import sys
import bottle
import picamera
from struct import Struct
from threading import Thread
from subprocess import Popen, PIPE
from time import sleep
from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication


### CONFIG - START
WS_PORT = 8084
HTTP_PORT = 8080
WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
bottle.debug(True)
### CONFIG - END


bottle.TEMPLATE_PATH.insert(0, os.path.join(os.path.dirname(__file__), 'templates'))
native_str = str
str = type('')

@bottle.route('/')
def IndexHandler():
    hostAddress=bottle.request.environ.get('HTTP_HOST')
    serverPort=bottle.request.environ.get('SERVER_PORT')
    wsAddress=hostAddress.replace(str(serverPort), str(WS_PORT))
    values = {
        'streamADDRESS': wsAddress,
        'WIDTH': WIDTH,
        'HEIGHT': HEIGHT,
    }
    return bottle.template('index.html', values)

@bottle.route('/cmd/<command>')
def CommandHandler(command):
    print("Befehl empfangen: %s" %command)
    #...mach damit irgendwas, zB gpio schalten

@bottle.route('/static/<filename>')
def send_static(filename):
    if filename.endswith(".css"):
        bottle.response.content_type = 'text/css'
    elif filename.endswith(".js"):
        bottle.response.content_type = 'text/javascript'
    elif filename.endswith(".png"):
        bottle.response.content_type = 'image/png'   
    return bottle.static_file(filename, root=os.path.join(os.path.dirname(__file__), 'static'))

class StreamingWebSocket(WebSocket):
    def opened(self):
        JSMPEG_MAGIC = b'jsmp'
        JSMPEG_HEADER = Struct(native_str('>4sHH'))
        self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, WIDTH, HEIGHT), binary=True)

class RaspiCamOutput(object):
    def __init__(self, camera):
        print('Spawning background conversion process')
        self.converter = Popen([
            'avconv',
            '-f', 'rawvideo',
            '-pix_fmt', 'yuv420p',
            '-s', '%dx%d' % camera.resolution,
            '-r', str(float(camera.framerate)),
            '-i', '-',
            '-f', 'mpeg1video',
            '-b', '800k',
            '-r', str(float(camera.framerate)),
            '-'],
            stdin=PIPE, stdout=PIPE, stderr=io.open(os.devnull, 'wb'),
            shell=False, close_fds=True)
    def write(self, b):
        self.converter.stdin.write(b)
    def flush(self):
        print('Waiting for background conversion process to exit')
        self.converter.stdin.close()
        self.converter.wait()

class BroadcastThread(Thread):
    def __init__(self, converter, websocket_server):
        super(BroadcastThread, self).__init__()
        self.converter = converter
        self.websocket_server = websocket_server
    def run(self):
        try:
            while True:
                buf = self.converter.stdout.read(512)
                if buf:
                    self.websocket_server.manager.broadcast(buf, binary=True)
                elif self.converter.poll() is not None:
                    break
        finally:
            self.converter.stdout.close()

if __name__ == '__main__':
    print('Initializing bottle thread')
    bottle_thread = Thread(target=bottle.run, kwargs=dict(host='0.0.0.0', port=HTTP_PORT, quiet=True))
    bottle_thread.daemon = True

    print('Initializing camera')
    with picamera.PiCamera() as camera:
        camera.resolution = (WIDTH, HEIGHT)
        camera.framerate = FRAMERATE
        camera.brightness = 50
        camera.contrast = 0
        sleep(1) # camera warm-up time

        print('Initializing websockets server on port %d' % WS_PORT)
        websocket_server = make_server(
            '', WS_PORT,
            server_class=WSGIServer,
            handler_class=WebSocketWSGIRequestHandler,
            app=WebSocketWSGIApplication(handler_cls=StreamingWebSocket)
        )
        websocket_server.initialize_websockets_manager()
        websocket_thread = Thread(target=websocket_server.serve_forever)

        print('Initializing broadcast thread')
        output = RaspiCamOutput(camera)
        broadcast_thread = BroadcastThread(output.converter, websocket_server)

        print('Starting recording')
        camera.start_recording(output, 'yuv')

        try:
            print('Starting bottle thread')
            bottle_thread.start()
            print('Starting websockets thread')
            websocket_thread.start()
            print('Starting broadcast thread')
            broadcast_thread.start()
            while True:
                camera.wait_recording(1)
        except KeyboardInterrupt:
            pass
        finally:
            print('Stopping recording')
            camera.stop_recording()
            print('Waiting for broadcast thread to finish')
            broadcast_thread.join()
            print('Shutting down websockets server')
            websocket_server.shutdown()
            print('Waiting for websockets thread to finish')
            websocket_thread.join()
            print('Waiting for bottle thread to finish')
            print("\nQuit\n")