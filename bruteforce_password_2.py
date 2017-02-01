#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This example is single-threaded so it can't take advantage of hyper threading, multiple CPUs or multiple CPU cores.
#
#   Version: 0.2
#   Creator: meigrafd
#   Copyright (C) 2017 by meiraspi@gmail.com published under the MIT License
#
from __future__ import print_function
import time
import string
import itertools

#attempt_limit = 99999999


try: #python2
    password = raw_input("Enter a password: ")
except: #python3
    password = input("Enter a password: ")


numbers = string.digits
uppers  = string.ascii_uppercase
lowers  = string.ascii_lowercase
symbols = string.punctuation
wspaces = string.whitespace

characters ="".join(numbers)
characters+="".join(uppers)
characters+="".join(lowers)
characters+="".join(symbols)
characters+="".join(wspaces)
base = len(characters)


def bruteforce(charset, maxlength):
    return (''.join(candidate)
        for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
        for i in range(1, maxlength + 1)))


solved=False
attempts=0
start = time.time()
for word in bruteforce(characters, base):
    if word == password:
        end = time.time()
        solved = True
        duration = round(end-start, 3)
        print('____Statistics____')
        print('Password: %s' % word)
        print('Attempts: %d' % attempts)
        print('Time: %d sec' % duration)
        print('Attempts per seconds: %d' % (attempts / duration))
        break
    else:
        attempts+=1
#    if attempts > attempt_limit:
#        break


if solved == False:
    print('unsolved after %d attempts' % attempts)




# EOF
