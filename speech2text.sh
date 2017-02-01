#!/bin/bash

## CONFIG - START

defaultLANG='en'

## CONFIG - END


if [ -z "$1" ]; then
	echo "No language supplied, using $defaultLANG"
	LANG=$defaultLANG
else
	echo "using $1 as language"
	LANG=$1
fi

API="http://www.google.com/speech-api/v1/recognize?lang=$LANG"

arecord -f cd -t wav -r 16000 -D plughw:1,0 | flac - -f --best --sample-rate 16000 -o out.flac

JSON=$(wget -O- --post-file out.flac --header="Content-Type: audio/x-flac; rate=16000" "$API")

UTTERANCE=`echo $JSON\
 |sed -e 's/[{}]/''/g'\
  |awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]; exit }'\
   |awk -F: 'NR==3 { print $3; exit }'\
    |sed -e 's/["]/''/g'`
echo "utterance: $UTTERANCE"


exit 0