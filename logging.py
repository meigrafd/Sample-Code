#
# http://www.forum-raspberrypi.de/Thread-python-switch-case-construct
#

import logging


logFileName = '/dev/shm/logfile.log'
loggingFormat = "%(asctime)s [%(levelname)-8s] [%(module)s:%(funcName)s:%(lineno)d]: %(message)s"

# ...

# switch...case replacement in python
logLevels = {
    "D": logging.DEBUG,
    "I": logging.INFO,
    "W": logging.WARNING,
    "E": logging.ERROR,
    "C": logging.CRITICAL
}

# Logger initialisieren:
logging.basicConfig(
    filename=logFileName,
    level=logging.DEBUG,
    datefmt="%d.%m.%Y %H:%M:%S",
    format=loggingFormat
)

logger = logging.getLogger()
logger.setLevel(logLevels["I"])

# ...

#
# Jetzt kommt von irgend woher (Konfig-File, Wert durch GPIO-Taste oder sonstwas)
# der einzustellende Loglevel als Ziffer zw. 1..4, nennen wir ihn "logLvlValue""
#
# Diesen Wert kann man jetzt mit einer if... elif.. else - Orgie abfragen und den Loglevel setzen..
# wird schnell unübersichtlich, wenn >10 Werte zu behandeln sind...

# Oder man verwendet das oben definierte Dictionary:

logger.setLevel(logLevels["D"])

#fertich..