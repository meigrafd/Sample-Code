#!/bin/bash
#
# http://www.ubuntu-forum.de/post/332500/cpu-load-bei-multi-core-prozessoren.html#post332500
#
# Anzahl der CPU Cores ermitteln
CPUCORES=$(grep ^processor /proc/cpuinfo | wc -l)
echo "Anzahl CPU Cores: "$CPUCORES

# Arrays fuer "vorherige Werte" initialisieren
for (( I=0; $I < $CPUCORES; I++ )); do
    TOTAL_LAST[$I]=0 
    BUSY_LAST[$I]=0
done

while true; do
    # Schleife ueber alle CPU Cores
    for (( I=0; $I < $CPUCORES; I++ )); do
        CPUDATA=$(grep ^"cpu"$I /proc/stat)
        BUSY_TICKS=$(echo $CPUDATA | awk -F' ' '{printf "%.0f", $2 + $3 + $4 + $7 + $8 - $BL}')   
        TOTAL_TICKS=$(echo $CPUDATA | awk -F' ' '{printf "%.0f", $2 + $3 + $4 + $5 + $6 + $7 + $8}')

        BUSY_1000=$((1000*($BUSY_TICKS-${BUSY_LAST[$I]})/($TOTAL_TICKS-${TOTAL_LAST[$I]})))
        BUSY_GANZZAHL=$(($BUSY_1000/10))
        BUSY_ZEHNTEL=$(($BUSY_1000))
        echo "CPU $I: $BUSY_GANZZAHL.$BUSY_ZEHNTEL %"

        # aktuelle Werte zwischenspeichern
        TOTAL_LAST[$I]=$TOTAL_TICKS
        BUSY_LAST[$I]=$BUSY_TICKS
    done
    echo
    # eine kleine Pause vor der naechsten Runde
    sleep 3
done

