#
#
# https://systemausfall.org/wikis/howto/Eddy-2-Power/Windmessger%C3%A4t
#
import time
import sys
from RPi import GPIO

class anemometer():
    def __init__(self):
        ''' initialize the pin for the anemometer sensor '''
        self.SENSOR_PIN = 4
        self.count = 0
        # tell the GPIO module that we want to use the chip's pin numbering scheme
        GPIO.setmode(GPIO.BCM)
        # setup pin as an input with pullup
        GPIO.setup(self.SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # threaded event, to detect voltage falling on anemometer
        # bouncetime is in ms - edges within this time will be ignored
        GPIO.add_event_detect(self.SENSOR_PIN, GPIO.FALLING, bouncetime=30)
        self.starttime = time.time()
        # deal with events by calling a function
        GPIO.add_event_callback(self.SENSOR_PIN, self.inputEventHandler)

    def inputEventHandler(self, pin):
        ''' count the edges and calculate windspeed...
            with "triggerflanke" you decide how much falling edges to count
            until we start the speed calculation
            small values will result in short reaction time und precise values
            high values will take longer and give a good average over the time
            very high values may need a longer sleep value in the main method
            espacially at low wind speeds
        '''
        self.count += 1
        triggerflanke = 10
        if self.count == triggerflanke:
            # the sensor ticks twice per rotation (2 falling edges)
            # so with triggerflanke=20 this happens after ten rotations
            currenttime = (time.time() - self.starttime)
            # calculating windspeed
            windspeed = triggerflanke / (currenttime * 1.3)
            # exit printing the windspeed
            sys.exit(windspeed)

    def cleanup(self):
        GPIO.cleanup() # don't leave a mess

if __name__ == "__main__":
    anemometer = anemometer()
    time.sleep(20)
    anemometer.cleanup()
    sys.exit(0) # no data - no wind - return 0
