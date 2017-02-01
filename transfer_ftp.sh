#!/bin/bash
#
# Titel: FTP Transfer Script
# Description: Datei automatisch auf einen festgelegten FTP-Server hochladen.
# Version: 0.1

### EINSTELLUNGEN

FTP_SERVER=Adresse_des_FTP-Servers ;#Bsp.: 192.168.0.100
FTP_USER=Benutzername
FTP_PASS=Passwort

#Die Datei(en) welche uebertragen werden soll
FILE2TRANSFER="/home/pi/Bild.jpg"

#Das Verzeichnis wohin die Datei uebertragen werden soll
REMOTEDIR=/var/www/picam/


### ENDE DER EINSTELLUNGEN


# Dateien per FTP auf den Server schieben
ftp -ni << END_UPLOAD
  open $FTP_SERVER
  user $FTP_USER $FTP_PASS
  cd $REMOTEDIR
  bin
  mput $FILE2TRANSFER
  quit
END_UPLOAD

exit 0