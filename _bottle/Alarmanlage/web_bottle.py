#!/usr/bin/python2
#
# http://www.forum-raspberrypi.de/Thread-html-webseite-zum-steuern-einer-alarmanlage?pid=248873#pid248873
# version: 2.0
#
from __future__ import print_function
import os.path
import bottle
import json
from datetime import datetime, timedelta
from RPi import GPIO

#------------------------------------------------------------------------

setting=dict()
setting["page_title"] = "Alarmanlage"
setting["no_motion_delay"] = 60
setting["DEBUG"] = True
webPort = 8080
PIR_PIN = 24
GPIO.setmode(GPIO.BCM)

#------------------------------------------------------------------------


def printD(message):
    if setting["DEBUG"]:
        print(message)


@bottle.route("/")
def IndexHandler():
    values = {
        "debug": setting["DEBUG"],
        "setting": setting,
    }
    return bottle.template("index.html", values)


@bottle.route("/cmd")
def CommandHandler():
    setting["armed"] = bottle.request.query.armed or setting["armed"]
    return bottle.redirect("/")


@bottle.route("/data/")
def TelemetryHandler():
    printD("Data Request.")
    bottle.response.content_type = "application/json"
    data=dict()
    data["ARMED"] = setting["armed"]
    if setting["motion"]:
        data["MOTION"] = setting["motion"]
    if setting["last_motion_time"]:
        data["MOTION_TIME"] = setting["last_motion_time"].strftime('%d.%m.%Y %H:%M:%S')
    return json.dumps(data)


@bottle.route("/static/<filename:path>")
def StaticHandler(filename):
    if filename.endswith(".css"):
        bottle.response.content_type = "text/css"
    elif filename.endswith(".js"):
        bottle.response.content_type = "text/javascript"
    elif filename.endswith(".png"):
        bottle.response.content_type = "image/png"   
    return bottle.static_file(filename, root=os.path.join(os.path.dirname(__file__), "static"))


@bottle.error(404)
def error404(error):
    return "Error 404: Nothing here, sorry."


def interrupt_event(pin):
    if setting["armed"] == "Ja":
        motion_time = datetime.now()
        if GPIO.input(PIR_PIN):
            setting["last_motion_time"] = motion_time
            if not setting["motion"] == "Ja":
                setting["motion"] = "Ja"
                printD("{} -> Motion detected!".format(motion_time.strftime('%d.%m.%Y %H:%M:%S')))
        else:
            if setting["motion"] == "Ja" and datetime.now() > (motion_time + timedelta(seconds=setting["no_motion_delay"])):
                setting["motion"] = "Nein"


try:
    setting["motion"] = "Nein"
    setting["last_motion_time"] = None
    setting["armed"] = "Nein"
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, callback=interrupt_event, bouncetime=100)
    bottle.TEMPLATE_PATH.insert(0, os.path.join(os.path.dirname(__file__), "templates"))
    bottle.run(host="0.0.0.0", port=webPort, quiet=False, debug=bool(setting["DEBUG"]))
except (KeyboardInterrupt, SystemExit):
    GPIO.cleanup()
    print("\nQuit\n")

#EOF