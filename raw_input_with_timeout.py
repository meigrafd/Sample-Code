# https://gist.github.com/atupal/5865237
# http://stackoverflow.com/a/3471853

import sys, time
from select import select

import platform
if platform.system() == "Windows":
    import msvcrt

def input_with_timeout_sane(prompt, timeout, default):
    """Read an input from the user or timeout"""
    print prompt,
    sys.stdout.flush()
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        s = sys.stdin.readline().replace('\n','')
    else:
        s = default
        print s
    return s

def input_with_timeout_windows(prompt, timeout, default): 
    start_time = time.time()
    print prompt,
    sys.stdout.flush()
    input = ''
    while True:
        if msvcrt.kbhit():
            chr = msvcrt.getche()
            if ord(chr) == 13: # enter_key
                break
            elif ord(chr) >= 32: #space_char
                input += chr
        if len(input) == 0 and (time.time() - start_time) > timeout:
            break
    if len(input) > 0:
        return input
    else:
        return default

def input_with_timeout(prompt, timeout, default=''):
    if platform.system() == "Windows":
        return input_with_timeout_windows(prompt, timeout, default)
    else:
        return input_with_timeout_sane(prompt, timeout, default)


eingabe = input_with_timeout("Enter something: ", 5)
if not eingabe:
    print "timeout"

#EOF