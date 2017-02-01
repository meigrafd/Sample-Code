#!/usr/bin/python3
import socket
from errno import ECONNREFUSED

def ping(host='127.0.0.1', port=80, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket().connect((host, port))
        print(str(port) + " Open")
        return True
    except socket.timeout as err:
        return False
    except socket.error as err:
        if err.errno == ECONNREFUSED:
            return False


#ping("192.168.0.10", 80)
#ping("216.58.213.14", 80, 1)
