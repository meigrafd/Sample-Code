import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 4096


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

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)
  conn, addr = s.accept()
  print 'Connection address:', addr
  while 1:
    if conn:
      data = conn.recv(BUFFER_SIZE).strip()
      if data:
        reqdata = ""
        print "received data:", data
        if data == "pitemp":
          reqdata = str(getTemp())
        elif data == "piram":
          reqdata = str(getPiRAM())
        else:
          reqdata = "UNKNOWN!"
        conn.send(reqdata + "\n")

except (KeyboardInterrupt, SystemExit):
  print("Schliesse Server..")
  s.close()
  conn.close()