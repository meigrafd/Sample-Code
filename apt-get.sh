#!/bin/bash

sudo apt-get update
NEW=$(sudo apt-get upgrade -s | grep "^Inst" | cut -d" " -f2-)
if [ ! -z "$NEW" ]; then
	IFS=$'\n'
	echo $NEW
fi

exit 0