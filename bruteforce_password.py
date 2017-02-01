#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# This example is single-threaded so it can't take advantage of hyper threading, multiple CPUs or multiple CPU cores.
#
#   Version: 0.1
#   Creator: meigrafd
#   Copyright (C) 2017 by meiraspi@gmail.com published under the MIT License
#
from __future__ import print_function
import time
import string


try:
    password = raw_input("Enter a password: ")
except:
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
base = len(characters)


# convert base 10 integer n into base b
def numberToBase(n, b):
    digits=[]
    while n:
        digits.append(int(n % b))
        n /= b
    return digits[::-1]


solved=False
attempts=0
start = time.time()
# test password, limited to 99,999,999 attempts
while (not solved) and (attempts < 99999999):
    lst = numberToBase(attempts, base)
    word=''
    for x in lst:
        word += characters[x]

    if password == word:
        end = time.time()
        solved = True
        duration = round(end-start, 3)
        print('____Statistics____')
        print('Password: %s' % word)
        print('Attempts: %d' % attempts)
        print('Time: %d sec' % duration)
        print('Attempts per seconds: %d' % (attempts / duration))
    else:
        attempts+=1

if solved == False:
    print('unsolved after %d attempts' % attempts)




# EOF
