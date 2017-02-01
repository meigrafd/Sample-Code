#!/bin/bash

GPIOpin=17

## init GPIOpin
if [ ! -f /sys/class/gpio/gpio${GPIOpin}/value ]; then
    echo $GPIOpin > /sys/class/gpio/export
    echo out > /sys/class/gpio/gpio${GPIOpin}/direction
fi

## monitor gpio state
while :; do
    ## get current state
    GPIOstate=$(</sys/class/gpio/gpio${GPIOpin}/value)

    ## switch state
    NEWstate=$(( ! $GPIOstate ))
    echo $NEWstate > /sys/class/gpio/gpio${GPIOpin}/value
    echo "switched GPIOpin $GPIOpin from $GPIOstate to $NEWstate"

    sleep 1
done