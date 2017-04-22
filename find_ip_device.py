#!/usr/bin/python2
#
# http://www.forum-raspberrypi.de/Thread-python-subprocess-check-output-mit-cut-und-grep
#
import shlex
from subprocess import Popen, PIPE
from datetime import datetime

def finde_geraet(IP='127.0.0.1', count=5):
    command = shlex.split('/usr/bin/nmap -F -Pn -sF %s' % IP)
    while count > 0:
        returncode=None
        found=False
        print "%s:  <%d>  Suche Gerät: %s" % (datetime.now(), count, IP)
        process = Popen(command, stdout=PIPE, stderr=PIPE, bufsize=1)
        for output in iter(process.stdout.readline, b''):
            if "host up)" in output.strip():
                found=True
        if process is not None:
            returncode = process.poll()
            process.stdout.close()
            process.wait()
        if found:
            return True
        if (returncode is not None) and (returncode != 0):
            print "Error! Returncode: %s" % returncode
        count -= 1
    return False


success_1 = finde_geraet('8.8.8.8')
success_2 = finde_geraet('10.8.0.20')
if not success_1 and not success_2:
    print "[%s]   KEIN GERÄT GEFUNDEN!" % datetime.now().strftime('%d.%m.%Y %H:%M:%S')


#EOF