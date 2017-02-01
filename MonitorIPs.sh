#!/bin/bash
#
DBfile=/var/db.sqlite
DBtable=monitor
TIMEOUT=1
#

[ ! -f $DBfile ] && echo "Error: No such file $DBfile" && exit 3

dbLIST=( $(sqlite3 $DBfile "SELECT ip FROM $DBtable WHERE 1") )
oldIFS=$IFS ; IFS=$'\n'
for ROW in "${dbLIST[@]}"; do
	IP=$(echo $ROW | awk '{split($0,a,"|"); print a[1]}')
	STATUS=offline
	echo -n "Checking IP: $IP"
	if [ -n "$(ping -q -W$TIMEOUT -c1 $IP | grep '1 received')" ]; then
		STATUS=Online
		DATETIME=$(date +%s)
		sqlite3 $DBfile "UPDATE $DBtable SET datetime=\"$DATETIME\",online=1 WHERE ip=\"$IP\""
	else
		# offline
		sqlite3 $DBfile "UPDATE $DBtable SET online='0' WHERE ip=\"$IP\""
	fi
	echo " -> $STATUS"
done
IFS=$oldIFS

exit 0