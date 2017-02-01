#!/usr/bin/python
#
#   Copyright (C) 2016 by meigrafd (meiraspi@gmail.com) published under the MIT License
#
import pigpio
import time

## CONFIG - START
RED_PIN   = 16
GREEN_PIN = 20
BLUE_PIN  = 21
STEPS = 1    # number of color changes per step (more is faster, less is slower)
## CONFIG - END

io = pigpio.pi()

def updateColor(color, step):
    color += step
    if color > 255:
        return 255
    if color < 0:
        return 0
    return color

def setLights(pin, brightness):
    realBrightness = int(int(brightness) * (float(bright) / 255.0))
    io.set_PWM_dutycycle(pin, realBrightness)

bright = 255
R = 255
G = 0
B = 0

setLights(RED_PIN, R)
setLights(GREEN_PIN, G)
setLights(BLUE_PIN, B)

while True:
    if R == 255 and G < 255 and B == 0:
        G = updateColor(G, STEPS)
        setLights(GREEN_PIN, G)

    elif R > 0 and G == 255 and B == 0:
        R = updateColor(R, -STEPS)
        setLights(RED_PIN, R)

    elif R == 0 and G == 255 and B < 255:
        B = updateColor(B, STEPS)
        setLights(BLUE_PIN, B)

    elif R == 0 and G > 0 and B == 255:
        G = updateColor(G, -STEPS)
        setLights(GREEN_PIN, G)

    elif R < 255 and G == 0 and B == 255:
        R = updateColor(R, STEPS)
        setLights(RED_PIN, R)

    elif R == 255 and G == 0 and B > 0:
        B = updateColor(B, -STEPS)
        setLights(BLUE_PIN, B)

setLights(RED_PIN, 0)
setLights(GREEN_PIN, 0)
setLights(BLUE_PIN, 0)

time.sleep(0.5)
io.stop()