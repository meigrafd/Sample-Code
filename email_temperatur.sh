#!/bin/bash
#
# v0.3 (c) by meigrafd
#
# http://www.forum-raspberrypi.de/Thread-shellscript-temperatursensor-auslesen-und-email-senden
#

#Mail Einstellungen
SMTPFROM='pi@anbieter.de' #Absender
SMTPTO='add@anbieter.de' #Empfänger
SMTPSERVER='mail.anbieter.de' #SMTP-Server
SMTPUSER='meinuser' #Benutzer
SMTPPASS='passwd' #Passwort
SMTPTLS=1
SUBJECT="Werte sind zu hoch!"
MSG="Die Luftfeuchtigkeit @%ORT% beträgt %HUM%% und die Temperatur beträgt %TEMP%*C"

#Sensor Variablen

#Format: 
#SENSOR[<GPIOpin>]="<Location>:<MAXtemp>:<MAXhum>:<Schwellenwert.fuer.Fehlmessungen>"
SENSOR[7]="Wohnzimmer:35:50:20"
SENSOR[11]="Schlafzimmer:35:50:20"
SENSOR[15]="Badezimmer:35:50:30"
SENSOR[18]="Dachboden:40:80:20"

# CONFIG - END

#----------------------------------------------------------------

#tmpfs fuer vorherige Messwerte anlegen um SD zu entlasten
if [ ! -d /var/humtemp ]; then
	echo "*** creating tmpfs /var/humtemp"
	sudo mkdir -p /var/humtemp
	sudo mount -t tmpfs tmpfs /var/humtemp -o defaults,size=1M
	sudo chmod 666 /var/humtemp
elif [ -z "$(grep /var/humtemp /proc/mounts)" ]; then
	echo "*** mounting tmpfs /var/humtemp"
	sudo mkdir -p /var/humtemp
	sudo mount -t tmpfs tmpfs /var/humtemp -o defaults,size=1M
	sudo chmod 666 /var/humtemp
fi

SENDMAIL=0
MESSAGE=""
for pin in ${!SENSOR[@]}; do
	sudo /home/pi/lol_dht22/loldht $pin > /var/humtemp/.output.DHT22
	if [ ! -z "$(grep 'Lock file is in use, waiting' /var/humtemp/.output.DHT22)" ]; then
		sudo killall -q -9 loldht
		sleep 5
		sudo /home/pi/lol_dht22/loldht $pin > /var/humtemp/.output.DHT22
	fi

	WERTE=$(grep Humidity /var/humtemp/.output.DHT22)
	Hum=$(echo $WERTE | awk {'print $3'})
	Temp=$(echo $WERTE | awk {'print $7'})
	LOCATION=$(echo ${SENSOR[$pin]} | awk -F':' {'print $1'})
	BADGAUGING=$(echo ${SENSOR[$pin]} | awk -F':' {'print $4'})

	#aktuelle Messung mit vorheriger (falls vorhanden) vergleichen um Fehlmessungen auszumerzen.
	if [ -f /var/humtemp/$LOCATION ]; then
		PREVhum=$(cat /var/humtemp/$LOCATION | awk -F':' {'print $1'})
		DIFF=$(echo "scale=0; $Hum - $PREVhum" | bc)
		if [ "$(echo "$DIFF > $BADGAUGING" | bc)" == 1 ]; then
			echo "$LOCATION: Offensichtliche Hum-Fehlmessung! Messwert $Hum wird ignoriert"
			continue
		fi
		PREVtemp=$(cat /var/humtemp/$LOCATION | awk -F':' {'print $2'})
		DIFF=$(echo "scale=0; $Temp - $PREVtemp" | bc)
		if [ "$(echo "$DIFF > $BADGAUGING" | bc)" == 1 ]; then
			echo "$LOCATION: Offensichtliche Temp-Fehlmessung! Messwert $Temp wird ignoriert"
			continue
		fi
	fi
	echo "$Hum:$Temp" > /var/humtemp/$LOCATION

	MAXtemp=$(echo ${SENSOR[$pin]} | awk -F':' {'print $2'})
	MAXhum=$(echo ${SENSOR[$pin]} | awk -F':' {'print $3'})
	echo "Place: $LOCATION -> Humidity: $Hum (max: $MAXhum) , Temperature: $Temp (max: $MAXtemp)"
	if [ "$(echo "$Hum > $MAXhum" | bc)" == 1 ]; then
		SENDMAIL=1
		tempMSG=${MSG//%ORT%/$LOCATION}
		tempMSG=${tempMSG//%HUM%/$Hum}
		tempMSG=${tempMSG//%TEMP%/$Temp}
		[ -z "$MESSAGE" ] && MESSAGE=$tempMSG || MESSAGE="$MESSAGE\n\r$tempMSG"
	fi
done

if [ $SENDMAIL == 1 ]; then
	echo "E-Mail wird verschickt"
	if [ -n "$SMTPTLS" ] && [ $SMTPTLS == 1 ]; then
		sendEmail -f $SMTPFROM -t $SMTPTO -u $SUBJECT -m $MESSAGE -o tls=yes -s $SMTPSERVER -xu "$SMTPUSER" -xp "$SMTPPASS"
	else
		sendEmail -f $SMTPFROM -t $SMTPTO -u $SUBJECT -m $MESSAGE -s $SMTPSERVER -xu "$SMTPUSER" -xp "$SMTPPASS"
	fi
fi