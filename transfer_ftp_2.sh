#!/bin/bash
#
# http://www.linux-community.de/Internal/Artikel/Print-Artikel/LinuxUser/2006/02/Dateitransfers-automatisieren/(article_body_offset)/2
#
logfile=/tmp/ftp.log
errorlog=/tmp/ftp.error
filelist="Bild1.jpg Bild2.jpg Video.avi"
#

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
for file in ${filelist}; do
	ftp -i -v  >> ${logfile} 2>&1 <<END_UPLOAD
		open 192.168.0.200
		bin
		lcd /home/pi
		cd /var/www/picam
		mput ${file}
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
