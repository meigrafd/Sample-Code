#!/bin/bash

### CONFIG - START


DIR=/path/to/dir/

# Speicher Angaben in MegaByte. 1024MB = 1GB
#( siehe: http://de.wikipedia.org/wiki/Byte#Vergleich )

Space_Max=1024

# Wie viel Speicher darf belegt sein?
#(es wird so viel geloescht bis diese Angabe ereicht wird)
Space_Min=512

# Loescht nur Files die aelter als ... Tage sind
Delete_Older=3


### CONFIG - END

CurrentSizeKB=$(du -sk $DIR | grep -o '[0-9]*')
CurrentSizeMB=$(( CurrentSizeKB / 1024 ))
DOsecs=$(( $Delete_Older * 86400 ))	;# 1 day = 86400 sec
nowEpoch=$(date +%s)

if [ ! $CurrentSizeKB -lt $(( $Space_Min * 1024 )) ]; then
	echo "Space used in ${DIR}: ${CurrentSizeMB}MB (${CurrentSizeKB}KB) out of ${Space_Max}MB max allowed."
	CleanedSpace=0
	for f in $(ls $DIR/*); do
		fEpoch=$(stat -c%Y $f)
		diff=$(( $nowEpoch - $fEpoch ))
		if [ $diff > $DOsecs ]; then
			fSize=$(du -sk $f | grep -o '[0-9]*')
			CleanedSpace=$(( $CleanedSpace + $fSize ))
			if [ $(( $fSize / 1024 )) == 0 ]; then
				echo "Deleting $(basename $f) to get ${fSize}KB space free."
			else
				echo "Deleting $(basename $f) to get $(( $fSize / 1024 ))MB space free."
			fi
			rm -f $f
			CurrentSizeKB=$(du -sk $DIR | grep -o '[0-9]*')
			[ $CurrentSizeKB -lt "$(( $Space_Min * 1024 ))" ] && break
		fi
	done
	if [ $CleanedSpace != 0 ]; then
		echo "Cleaned $(( $CleanedSpace / 1024 ))MB (${CleanedSpace}KB) Space."
	else
		echo "No Files for Cleanup (older than ${Delete_Older}days) found!"
	fi
fi

exit 0