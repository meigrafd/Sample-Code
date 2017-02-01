#!/bin/bash
# http://www.forum-raspberrypi.de/Thread-kamera-modul-twitch-stream?pid=203139#pid203139

STREAM_KEY='xxxxxxx'
STREAM_URL="rtmp://live.twitch.tv/app/${STREAM_KEY}"
INRES="1920x1080"         # Input resolution
OUTRES="960x540"        # Output resolution
FPS=15
INPUT="rawvideo"
PIXEL="-pix_fmt yuv420p" #sets pixel format to Y'UV420p. Otherwise by default Y'UV444 is used and is incompatible with twitch
#INPUT="video4linux2"
#INPUT=x11grab  # -i :0.0
#CODEC=mpeg1video
CODEC=flv
THREADS="-threads 0"    #(0 autostarts threads based on cpu cores)
BUFFER="-bufsize 512k"
QUALITY="fast"     # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo
CBR="1000k"
GOP=$((FPS * 2))
GOPMIN="24"
#BIN=ffmpeg
BIN=avconv

# http://unix.stackexchange.com/a/195302

echo "Starting twitch.tv stream"
$BIN \
    -f $INPUT $PIXEL -s "$INRES" -r "$FPS" \
    -i /dev/video0 -vcodec libx264 -tune film \
    -s "$OUTRES" -preset "$QUALITY" -g $GOP -keyint_min "$GOPMIN" \
    -b:v $CBR -minrate "$CBR" -maxrate "$CBR" \
    -acodec libmp3lame $THREADS -strict normal \
    $BUFFER -crf 23 -r "$FPS" \
    -f $CODEC "$STREAM_URL"

exit 0