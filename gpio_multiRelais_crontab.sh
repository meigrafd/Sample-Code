#!/bin/bash
#
# Copyright (C) 2016 by meigrafd (meiraspi@gmail.com) published under the MIT License
#
# http://www.forum-raspberrypi.de/Thread-raspbian-anzahl-der-datensaetze-in-crontab
#

### --- Config - Start

# GPIO und Zeit Zuordnung
# Format: Relais[gpio]="Tag,hEin,hAus"
# Tag: 0 = Sonntag, 6 = Samstag
Relais[2]="1,08:30,09:15"
Relais[3]="2,08:30,09:15"
Relais[4]="2,12:00,22:45"
Relais[17]="4,12:00,22:45"

# Erstelle Logfile? [0 = Nein, 1 = Ja]
LOG=1
# Maximale Logfile Grösse in Bytes? (leer lassen falls unbegrenzt) (512000 bytes = 500 kilobytes = 0.48 megabytes)
MAXLOGSIZE=""
# falls MAXLOGSIZE genutzt wird: Logfile rotieren[1] oder löschen[0]?
LOGROTATE=1

LOGFILE="./log.$(basename $0)"

### --- Config - End


### --- functions

Init_GPIO() {
    local pin=$1
    local direction=$2
    if [ ! -f /sys/class/gpio/gpio${pin}/value ]; then
        echo $pin > /sys/class/gpio/export
        echo $direction > /sys/class/gpio/gpio${pin}/direction
    fi
}

# check and write log / also echo message to console
function _LOG() {
    message="$1"
    _DT=$(date +"%d.%m.%Y %H:%M:%S")
    echo -e "[$_DT] \t $message"
    if [ $LOG = "1" ]; then
        #check size of logfile
        if [ -n "$MAXLOGSIZE" ] && [ -f "$LOGFILE" ] && [ "$(stat --printf="%s" $LOGFILE)" -gt "$MAXLOGSIZE" ]; then
            if [ "$LOGROTATE" = 1 ]; then
                echo "Rotating log $LOGFILE"
                echo "[$_DT] Rotating log $LOGFILE" >> $LOGFILE
                mv -f $LOGFILE ${LOGFILE}.1 >/dev/null 2>&1
            else
                echo "Resetting/Deleting log $LOGFILE"
                rm -f $LOGFILE >/dev/null 2>&1
            fi
            touch $LOGFILE
        fi
        echo "[$_DT]  $message" >> $LOGFILE
    fi
}

## ---

currentWeekDay=$(date +%u)
currentHour=$(date +%H)
currentMinute=$(date +%M)

for gpio in ${!Relais[@]}; do
    Init_GPIO $gpio out
    weekDay=${Relais[gpio]%%,*}
    [ "$currentWeekDay" != "$weekDay" ] && continue
    temp=$(echo ${Relais[gpio]} | tr , ' ')
    onTime=$(echo $temp | awk '{print $2}')
    offTime=$(echo $temp | awk '{print $3}')
    onHour=${onTime%%:*}
    onMinute=${onTime##*:}
    offHour=${offTime%%:*}
    offMinute=${offTime##*:}
    if [ "$onHour" == "$currentHour" ] && [ "$onMinute" == "$currentMinute" ]; then
        _LOG "Turning relais gpio $gpio on"
        echo 1 > /sys/class/gpio/gpio${gpio}/value
    elif [ "$offHour" == "$currentHour" ] && [ "$offMinute" == "$currentMinute" ]; then
        _LOG "Turning relais gpio $gpio off"
        echo 0 > /sys/class/gpio/gpio${gpio}/value
    else
        echo -e "[$(date +"%d.%m.%Y %H:%M:%S")] \t Nothing to do.."
    fi
done

exit 0