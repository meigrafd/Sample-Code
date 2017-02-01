#!/bin/sh

# get rid of the cursor so we don't see it when videos are running
setterm -cursor off

# set here the path to the directory containing your videos
VIDEOPATH="/home/pi/videos" 

# you can normally leave this alone
SERVICE="omxplayer"

# optional Parameters for SERVICE
OPTIONS=""

# now for our infinite loop!
while true; do
	if ps ax | grep -v grep | grep $SERVICE > /dev/null
	then
		sleep 1;
	else
		for File in $VIDEOPATH/*
		do
			clear
			$SERVICE $OPTIONS $File > /dev/null
		done
	fi
done