#!/usr/bin/python3
#
# http://www.forum-raspberrypi.de/Thread-tutorial-ansteuerung-einer-7-segment-anzeige
#
from six.moves import input
from RPi import GPIO


GPIO.setmode(GPIO.BOARD)

gpios = {
    'left_above': 24,
    'left_below': 21,
    'middle_above': 23,
    'middle_middle': 26,
    'middle_below': 19,
    'right_above': 22,
    'right_below': 18,
    'dot': 16,
}

numbers = {
    0: [
            gpios['left_above'],
            gpios['left_below'],
            gpios['middle_above'],
            gpios['middle_below'],
            gpios['right_above'],
            gpios['right_below'],
       ],
    1: [
            gpios['left_above'],
            gpios['left_below'],
       ],
    2: [
            gpios['left_below'],
            gpios['middle_above'],
            gpios['middle_middle'],
            gpios['middle_below'],
            gpios['right_above'],
       ],
    3: [
            gpios['left_above'],
            gpios['middle_above'],
            gpios['middle_middle'],
            gpios['middle_below'],
            gpios['right_above'],
            gpios['right_below'],
       ],
    4: [
            gpios['left_above'],
            gpios['middle_middle'],
            gpios['right_above'],
            gpios['right_below'],
       ],
    5: [
            gpios['left_above'],
            gpios['middle_above'],
            gpios['middle_middle'],
            gpios['middle_below'],
            gpios['right_below'],
       ],
    6: [
            gpios['left_above'],
            gpios['left_below'],
            gpios['middle_above'],
            gpios['middle_middle'],
            gpios['middle_below'],
            gpios['right_below'],
       ],
    7: [
            gpios['middle_above'],
            gpios['right_above'],
            gpios['right_below'],
       ],
    8: [
            gpios['left_above'],
            gpios['left_below'],
            gpios['middle_above'],
            gpios['middle_middle'],
            gpios['middle_below'],
            gpios['right_above'],
            gpios['right_below'],
       ],
    9: [
            gpios['left_above'],
            gpios['middle_above'],
            gpios['middle_middle'],
            gpios['right_above'],
            gpios['right_below'],
       ]
}


def gpio_setup(gpio_list):
    for pin in gpio_list.values():
        GPIO.setup(pin, GPIO.OUT)


def reset_gpios(gpio_list):
    for pin in gpio_list.values():
        GPIO.output(pin, 0)


def set_gpios_digit(dig):
    for pin in numbers[dig]:
        GPIO.output(pin, 1)


def show_value(value):
    n = [char for char in str(value)]
    #n.reverse()
    for char in n:
        if char.isdigit():
            set_gpios_digit(int(char))


def run():
    gpio_setup(gpios)
    while True:
        val = str(input('Bitte Wert eingeben: '))
        reset_gpios(gpios)
        show_value(val)


if __name__ == '__main__':
    run()

# EOF
