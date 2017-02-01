#!/bin/bash

declare -A GPIO
GPIO['a']=17    ;#red
GPIO['1']=22    ;#green


## init GPIOpin
for key in ${!GPIO[@]}; do
    if [ ! -f /sys/class/gpio/gpio${GPIO[$key]}/value ]; then    
        echo ${GPIO[$key]} > /sys/class/gpio/export    
        echo out > /sys/class/gpio/gpio${GPIO[$key]}/direction    
    fi
done


function schalten() {
    ## get current state
    local GPIOstate=$(cat /sys/class/gpio/gpio${1}/value)

    ## switch state
    local NEWstate=$(( ! $GPIOstate ))
    echo $NEWstate > /sys/class/gpio/gpio${1}/value
    echo "switched GPIOpin $1 from $GPIOstate to $NEWstate"
}

function _exit() {
    stty sane
    #echo -e '\nQuit\n'
    exit 0
}
trap _exit SIGHUP SIGINT SIGTERM EXIT

#stty -echo -icanon -icrnl time 0 min 0
stty -echo

while :; do
    read -n 1 keypress
    if [ "$keypress" == "a" ]; then
        echo "Key 'a' is pressed"
        schalten ${GPIO[$keypress]}
    elif [ "$keypress" == "1" ]; then
        echo "Key '1' is pressed"
        schalten ${GPIO[$keypress]}
    else
        echo "Unknown key: $keypress"
    fi
done
