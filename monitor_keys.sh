#!/bin/bash
#
# http://www.forum-raspberrypi.de/Thread-shellscript-script-zum-auslesen-und-anzeigen-von-tastatur-tasten?pid=151164#pid151164
# 
 
function identify_key {
 
    local key="$@"
    local printable=""
     
    case "$key" in
       "1b") echo "ESC ($key)";;
       "09") echo "TAB ($key)";;
       "1b 1b") echo "DOUBLE ESC ($key)";;
       "7f") echo "BKS ($key)";;
       "1b 5b 41") echo "UP ($key)";;
     
       "1b 5b 42") echo "DOWN ($key)";;
       "1b 5b 43") echo "RIGHT ($key)";;
       "1b 5b 44") echo "LEFT ($key)";;
     
       "1b 5b 47") echo "NUM5 ($key)";;
       "1b 5b 50") echo "PAUSE ($key)";;
     
       "1b 5b 31 7e") echo "HOME ($key)";;
       "1b 5b 32 7e") echo "INS ($key)";;
       "1b 5b 33 7e") echo "DEL ($key)";;
       "1b 5b 34 7e") echo "END ($key)";;
       "1b 5b 35 7e") echo "PGUP ($key)";;
       "1b 5b 36 7e") echo "PGDN ($key)";;
     
       "1b 5b 5b 41") echo "F1 ($key)";;
       "1b 5b 5b 42") echo "F2 ($key)";;
       "1b 5b 5b 43") echo "F3 ($key)";;
       "1b 5b 5b 44") echo "F4 ($key)";;
       "1b 5b 5b 45") echo "F5 ($key)";;
       "1b 5b 31 37 7e") echo "F6 ($key)";;
       "1b 5b 31 38 7e") echo "F7 ($key)";;
       "1b 5b 31 39 7e") echo "F8 ($key)";;
       "1b 5b 32 30 7e") echo "F9 ($key)";;
       "1b 5b 32 31 7e") echo "F10 ($key)";;
       "1b 5b 32 33 7e") echo "F11 ($key)";;
       "1b 5b 32 34 7e") echo "F12 ($key)";;
     
       "1b 1b 5b 5b 41") echo "ALT+F1 ($key)";;
       "1b 1b 5b 5b 42") echo "ALT+F2 ($key)";;
       "1b 1b 5b 5b 43") echo "ALT+F3 ($key)";;
       "1b 1b 5b 5b 44") echo "ALT+F4 ($key)";;
       "1b 1b 5b 5b 45") echo "ALT+F5 ($key)";;
       "1b 1b 5b 31 37 7e") echo "ALT+F6 ($key)";;
       "1b 1b 5b 31 38 7e") echo "ALT+F7 ($key)";;
       "1b 1b 5b 31 39 7e") echo "ALT+F8 ($key)";;
       "1b 1b 5b 32 30 7e") echo "ALT+F9 ($key)";;
       "1b 1b 5b 32 31 7e") echo "ALT+F10 ($key)";;
       "1b 1b 5b 32 33 7e") echo "ALT+F11 ($key)";;
       "1b 1b 5b 32 34 7e") echo "ALT+F12 ($key)";;
       "") echo "SPACE or INTRO";;
       *) # check if it's ALT+xx
          if [ ${#key} -gt 2 ] && [ "${key:0:2}" == "1b" ]; then
             # if string length greather than 2 and starts by Escape (1b)
             printable="\x"${key:3}   # erases the starting '1b ' 
             printf "ALT+%b (%s)\n" "$printable" "$key"
          else
             printable="\x"$key
             printf "%b (%s)\n" "$printable" "$key"
          fi
          ;;
    esac
}
 
 
 
function key_5b {
  # process '1b 5b ...' keys and return values
 
  local key=$1
  local keyA=""
  local keyB=""
  local keyC=""
 
  keyA=`echo -n "$key" |  hexdump -ve '1/1 "%.2x\n"'`; key=""
  case "$keyA" in
     "31" | "32" | "33" | "34" | "35" | "36") # Must read the following key
             read -rsn1 -t 1 key   # Wait 1 second max for next key
             if [ "$key" == "" ]; then
                # 'ESC + [ + A|B|C|....F' keys pressed (very fast)
                 echo "$keyA"
             else
                 keyB=`echo -n "$key" |  hexdump -ve '1/1 "%.2x\n"'`; key=""
                 if [ "$keyB" == "7e" ]; then
                    # got '~', uses to be the last key so return "XX 7e" where XX is [31|32|33|34|35|36]
                    echo "$keyA $keyB"
                 else
                    read -rsn1 -t 1 key   # Wait 1 second max for next key
                    if [ "$key" == "" ]; then
                       # 'A|B|C|....F + XX' keys pressed (very fast)
                       echo "$keyA $keyB"
                    else
                       keyC=`echo -n "$key" |  hexdump -ve '1/1 "%.2x\n"'`; key=""
                       # max depth level, so return
                       echo "$keyA $keyB $keyC"
                    fi
                 fi
              fi
              ;;
        "5b") # read another key and return (uses to be F1 ... F5 keys) '1b 5b 5b [41|42|43|44|45]'
              read -rsn1 -t 1 key   # Wait 1 second max for next key
              keyB=`echo -n "$key" |  hexdump -ve '1/1 "%.2x\n"'`; key=""
              echo "$keyA $keyB"
              ;;
           *) # Uses to be UP or other arrow keys '1b 5b [41|42|43|44]' so return
              echo "$keyA"
              ;;
  esac
}
 
 
 
function getkey {
  local key=""
  local key1=""
  local key2=""
  local key3=""
  local key4=""

  oldifs="$IFS"
  IFS=" "

  read -rsn1 key
  key1=`echo -n "$key" |  hexdump -ve '1/1 "%.2x\n"'`; key=""
  if [ "$key1" == "1b" ]; then
     read -rsn1 -t 1 key   # Wait 1 second max for next key
     if [ ! "$key" == "" ]; then
        key2=`echo -n "$key" |  hexdump -ve '1/1 "%.2x\n"'`; key=""
        case "$key2" in
           "1b") # it could be a double ESC or an ALT+Fx key
                 read -rsn1 -t 1 key   # Wait 1 second max for next key
                 if [ "$key" == "" ]; then
                    # "1b 1b" 'ESC' key pressed 2 times (very fast)
                    echo "$key1 $key2"
                 else
                    # "1b 1b ..." Uses to be ALT+F? key pressed
                    key3=`echo -n "$key" |  hexdump -ve '1/1 "%.2x\n"'`; key=""
                    if [ "$key3" == "5b" ]; then
                       read -rsn1 -t 1 key   # Wait 1 second max for next key
                       if [ "$key" == "" ]; then
                          # "1b 1b 5b" 'ESC + ESC + [' keys pressed (very fast)
                          echo "$key1 $key2 $key3"
                       else
                          echo "$key1 $key2 $key3 $(key_5b $key)"
                       fi
 
                    else
                       # Unknown key '1b 1b XX' so return
                       echo "$key1 $key2 $key3"
                    fi
                 fi
                 ;;
           "5b") # Several posibilities "1b 5b ..."
                 read -rsn1 -t 1 key   # Wait 1 second max for next key
                 if [ "$key" == "" ]; then
                    # "1b 5b" 'ESC + [' keys pressed (very fast)
                    echo "$key1 $key2"
                 else
                    echo "$key1 $key2 $(key_5b $key)"
                 fi
 
                 ;;
              *) # ESC + Other key pressed (very fast) or ALT+xx
                 echo "$key1 $key2"
                 ;;
        esac
     else
        # ESC key pressed
        echo "$key1"
     fi
  else
     echo "$key1"
  fi
 
  IFS="$oldifs"
  return 0
}
 
 
while true; do
  echo "----------------------------"
  tecla=$(getkey)
  identify_key $tecla
done