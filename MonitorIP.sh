#!/bin/bash
#
DBfile=/var/db.sqlite
DBtable=monitor
#

[ ! -f $DBfile ] && sqlite3 $DBfile "CREATE TABLE IF NOT EXISTS $DBtable (id INTEGER PRIMARY KEY,ip TEXT,online INT,datetime INT)"

case $1 in
	add)
		[ -z "$2" ] && echo "Usage: $(basename $0) add <IP>" && exit 1
		Added=$(sqlite3 $DBfile "SELECT ip FROM $DBtable WHERE ip=\"$2\"")
		[ ! -z "$Added" ] && echo "IP $2 is already added!" && exit 1
		sqlite3 $DBfile "INSERT INTO $DBtable (ip,online,datetime) VALUES (\"$2\",\"0\",\"$(date +%s)\")"
		[ $? -ne "0" ] && echo "Error while adding IP $2" || echo "Successfully added IP $2"
	;;
	del)
		[ -z "$2" ] && echo "Usage: $(basename $0) del <IP> (all)" && exit 1
		if [ "$2" = "all" ]; then
			COUNT=0
			dbLIST=( $(sqlite3 $DBfile "SELECT id FROM $DBtable WHERE 1") )
			oldIFS=$IFS ; IFS=$'\n'
			for ROW in "${dbLIST[@]}"; do
				ID=$(echo $ROW | awk '{split($0,a,"|"); print a[1]}')
				sqlite3 $DBfile "DELETE FROM $DBtable WHERE id=\"$ID\""
				COUNT=$(($COUNT + 1))
			done
			echo "Deleted $COUNT IP's!"
		else
			Added=$(sqlite3 $DBfile "SELECT ip FROM $DBtable WHERE ip=\"$2\"")
			[ -z "$Added" ] && echo "IP $2 is not added!" && exit 1
			sqlite3 $DBfile "DELETE FROM $DBtable WHERE ip=\"$2\""
			[ $? -ne "0" ] && echo "Error while deleting IP $2" || echo "Successfully deleted IP $2"
		fi
	;;
	list)
		dbLIST=( $(sqlite3 $DBfile "SELECT * FROM $DBtable WHERE 1") )
		oldIFS=$IFS ; IFS=$'\n'
		for ROW in "${dbLIST[@]}"; do
		    ID=$(echo $ROW | awk '{split($0,a,"|"); print a[1]}')
		    IP=$(echo $ROW | awk '{split($0,a,"|"); print a[2]}')
		    ONLINE=$(echo $ROW | awk '{split($0,a,"|"); print a[3]}')
		    DT=$(echo $ROW | awk '{split($0,a,"|"); print a[4]}')
		    echo "$ID) IP: $IP -> Online: $ONLINE -> Added/Checked: $(date -d@$DT +'%d.%m.%Y %H:%M:%S')";
		done
		IFS=$oldIFS
	;;
	*)
		echo "Usage: $(basename $0) [add|del|list] <IP>"
		exit 1
	;;
esac

exit 0