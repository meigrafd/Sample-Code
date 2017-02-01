#!/bin/bash
#
# crontab: * * * * * /bin/bash /path/to/lueftersteuerung.sh >/dev/null 2>&1
#
Max_Temp=60
Min_Temp=50

#gpio pin zur transistor-basis um gnd fuer den luefter zu schalten
GPIOpin=17

######

LUEFTER_DATEI=/tmp/luefterstatus.txt
TEMP_DATEI=/tmp/temperatur.txt

## init GPIOpin
if [ ! -f /sys/class/gpio/gpio${GPIOpin}/value ]; then
    echo $GPIOpin > /sys/class/gpio/export
    echo out > /sys/class/gpio/gpio${GPIOpin}/direction
fi

[ -f $LUEFTER_DATEI ] && LuefterStatus=$(cat $LUEFTER_DATEI) || LuefterStatus=0
Temp=$(cat /sys/class/thermal/thermal_zone0/temp)
CurrentTemp=$(echo "scale=2; $Temp / 1000" | bc)
CurrentTemp2=$(echo $CurrentTemp | awk -F. {'print $1'})

#Debug
#echo -e "CurrentTemp: $CurrentTemp °C \nLuefterStatus: $LuefterStatus"

if [ $CurrentTemp2 -gt $Max_Temp ] && [ $LuefterStatus -eq 0 ]; then
	echo "CurrentTemp $CurrentTemp > Max_Temp $Max_Temp ... Luefter werden eingeschaltet"
	#Luefter einschalten
	echo 1 > /sys/class/gpio/gpio${GPIOpin}/value
	echo 1 > $LUEFTER_DATEI
elif [ $CurrentTemp2 -gt $Min_Temp ] && [ $LuefterStatus -eq 1 ]; then
	echo "CurrentTemp $CurrentTemp > Min_Temp $Min_Temp ... Luefter bleiben eingeschaltet"
elif [ $CurrentTemp2 -le $Min_Temp ] && [ $LuefterStatus -eq 1 ]; then
	echo "CurrentTemp $CurrentTemp < Min_Temp $Min_Temp ... Luefter werden ausgeschaltet"
	#Luefter ausschalten
	echo 0 > /sys/class/gpio/gpio${GPIOpin}/value
	echo 0 > $LUEFTER_DATEI
fi

echo $CurrentTemp > $TEMP_DATEI

exit 0