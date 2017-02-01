#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
import sys
import socket
import subprocess
#import signal
try:
  import SocketServer as socketserver
except ImportError:
  import socketserver

#-------------------------------------------------------------------
DEBUG = True
#DEBUG = False
SocketHost = "0.0.0.0"
SocketPort = 5000
#-------------------------------------------------------------------

# thread docu: http://www.tutorialspoint.com/python/python_multithreading.htm
# signal docu: http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
# socketserver docu: https://docs.python.org/2/library/socketserver.html

#-------------------------------------------------------------------

try:
  DEBUG
except NameError:
  DEBUG = False

if DEBUG:
  print("Enabling DEBUG mode!")
else:
  print("Disabling DEBUG mode!")

def printD(message):
  if DEBUG:
    print(message)
    sys.stdout.flush()


# Raspberry CPU Temperatur
def getTemp():
  with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
    CPUtemp = int(float(f.readline().split()[0]))
    CPUtemp = round((CPUtemp/1000.0), 2)
    return CPUtemp

def getUptime():
  with open('/proc/uptime', 'r') as f:
    uptime_seconds = float(f.readline().split()[0])
    uptime = str(timedelta(seconds = uptime_seconds))
  return uptime

def getPiRAM():
  with open('/proc/meminfo', 'r') as mem:
    tmp = 0
    for i in mem:
      sline = i.split()
      if str(sline[0]) == 'MemTotal:':
        total = int(sline[1])
      elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
        tmp += int(sline[1])
    free = tmp
    used = int(total) - int(free)
    usedPerc = (used * 100) / total
    return usedPerc

#perform Socket request
def ParseSocketRequest(request):
  #printD("Parsing SocketRequest: "+request)
  returnlist = ""
  request = request.strip()
  if request == "ping":
    returnlist += "\n pong"
  elif request == "pitemp":
    returnlist += "\n %s" % getTemp()
  return returnlist

#socket server <-> client
class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
  def handle(self):
    # self.rfile is a file-like object created by the handler;
    # we can now use e.g. readline() instead of raw recv() calls
    self.data = self.rfile.readline().strip()
    printD("SocketRequest: {}".format(self.data))
    try:
      self.wfile.write(ParseSocketRequest(self.data))
    except Exception, e2:
      print("Error in ThreadedTCPRequestHandler: " + str(e2))
    except (KeyboardInterrupt, SystemExit):
      _exit()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
  pass


if __name__ == '__main__':
  try:
    HOST, PORT = SocketHost, SocketPort
    socket_server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = socket_server.server_address
    # Start a thread with the server - that thread will then start one more thread for each request
    socket_server_thread = threading.Thread(target=socket_server.serve_forever)
    socket_server_thread.start()
    print("socket_server_thread ist aktiv: %s" % socket_server_thread.isAlive())
    #print("Socket Server loop running in thread: %s" % socket_server_thread.name)
    #thread_count = threading.active_count()
    #print("Insgesamt sind %s Threads aktiv." % thread_count)
  except Exception, e1:
    print("Error...: " + str(e1))
  except (KeyboardInterrupt, SystemExit):
    print("Schliesse Programm..")
    _exit()

def _exit():
  try:
    sys.exit()
  except Exception, e3:
    exit()

# this is the main thread which exits after all is done, so Dont close it here!
