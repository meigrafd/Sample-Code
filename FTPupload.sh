#!/bin/bash
#
# http://www.forum-raspberrypi.de/Thread-tutorial-automatisierte-dateiuebertragung-ftp-sftp-scp-usw
#
### EINSTELLUNGEN
#
FTP_SERVER=Hostname_des_FTP-Servers_aus_netrc   #Bsp.: 192.168.0.200

#Die Datei welche uebertragen werden soll
FILE2TRANSFER="/home/pi/Bild1.jpg /home/pi/Bild2.jpg /home/pi/Bild2.jpg"

#Das Verzeichnis wohin die Datei uebertragen werden soll
REMOTEDIR=/var/www/picam/

logfile=/tmp/ftp.log
errorlog=/tmp/ftp.error
#
### ENDE DER EINSTELLUNGEN

## Return Codes
#(bash v3 doesnt support declare -A)
ReturnCodes=(
    '202::Befehl nicht implementiert.'
    '421::Dienst nicht verfuegbar.'
    '426::Transfer abgebrochen.'
    '450::Datei nicht verfuegbar.'
    '500::Syntaxfehler.'
    '501::Syntaxfehler in Argumenten.'
    '503::Benutzer nicht angemeldet.'
    '550::Datei nicht verfuegbar.'
    '553::Ungueltiger Dateiname.'
    '666::Datei oder Verzeichnis existiert nicht.'
    '777::Unbekannter Host.'
    '999::Ungueltiger Befehl.'
)

function ReturnCode() {
    RC=$1
    [[ "$RC" =~ ':' ]] && RC=$(echo $RC | sed -e s/.*://)
    [[ "$RC" =~ ' ' ]] && RC=$(echo $RC | awk {'print $1'})
    for index in "${ReturnCodes[@]}" ; do
        KEY="${index%%::*}"
        VALUE="${index##*::}"
        [[ "$KEY" == "$RC" ]] && echo "$VALUE" && break
    done
}

rm -f ${logfile}
for file in ${FILE2TRANSFER}; do
	localDir=$(dirname $file)
	localFile=$(basename $file)
    ftp -i -v  >> ${logfile} 2>&1 <<END_UPLOAD
        open $FTP_SERVER
        bin
        lcd $localDir
        cd $REMOTEDIR
        mput ${localFile}
        quit
    END_UPLOAD
done

rm -f ${errorlog}
IFS=$'\n'
for line in $(cat ${logfile}); do
    ReturnCode "$line" >> ${errorlog}
done

if [ -f ${errorlog} ] && [ "$(stat --printf="%s" ${errorlog})" -gt "0" ]; then
    echo -e "ERROR:\n$(cat ${errorlog})"
    exit 1
else
    echo OK
    exit 0
fi