#!/bin/bash
# 06.2015 by meigrafd
#
### CONFIG - START
UsersPrefix=Benutzer
UsersCounts=30
UsersHomedir=/home/
UsersShell=/bin/bash
UsersGroupID=100
UsersPassword='Username'
### CONFIG - END

### functions
function addUsers {
	[ -z "$1" ] && CreateCount=$UsersCounts || CreateCount=$1
	echo "Creating $CreateCount Users with HOME:$UsersHomedir SHELL:$UsersShell PASSWD:$UsersPassword"
	echo
	for (( count=1; count<=$CreateCount; count++ )); do
		NewUser=$UserPrefix$count
		echo "Adding User '$UserPrefix$count' ..."
		#useradd -l -N -b$UsersHomedir$NewUser -m -s$UsersShell -g$UsersGroupID -p $(echo "$UsersPassword" | openssl passwd -1 -stdin)
		useradd -l -N -b$UsersHomedir$NewUser -m -s$UsersShell -g$UsersGroupID
		echo "$NewUser:$UsersPassword" | chpasswd --md5 $NewUser
		## also add user to samba:
		#echo -e "$UsersPassword\n$UsersPassword" | pdbedit -t -u $NewUser
	done
}

function delUsers {
	[ -z "$1" ] && CreateCount=$UsersCounts || CreateCount=$1
	echo "Deleting $CreateCount Users ..."
	for (( count=1; count<=$CreateCount; count++ )); do
		userdel -f -r $UserPrefix$count >/dev/null 2>&1
	done
}

case "$1" in
	add)	addUsers $2;;
	del)	delUsers $2;;
	*)	echo "Usage: $(basename $0) {add|del}" && exit 1;;
esac

exit 0