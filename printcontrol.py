#!/usr/bin/env python

from sys import argv
from octoclient import OctoClient
from api_keys import URL, API_KEY
import os
from os.path import dirname

# Pause the printer
def pause_print():
    try:
        client = OctoClient(url=URL, apikey=API_KEY)
        flags = client.printer()['state']['flags']
        if flags['printing']:
            client.pause()
            print("Print paused.")
            print("Layer: " + str(LAYER))
        elif flags['paused'] or flags['pausing']:
            print("Print already paused.")
        else:
            print("Print cancelled or error occurred.")
    except Exception as e:
        print(e)

print(argv)
if len(argv) < 2:
    exit()

if argv[2] == 'nan': # Exit if SCORE is NaN, this occurs on the background and first layer
    img_file = str(argv[3])
    logfile = dirname(img_file) + '/output.log'
    os.system("sed -i '/g$/d' {}".format(logfile))
    exit()

# Get SCORE, DEVIANCE and current layer from get_score.py

LAYER = int(argv[1])
# Do nothing if it is the background or first layer
if LAYER <= 7:
    img_file = str(argv[6])
    logfile = dirname(img_file) + '/output.log'
    os.system("sed -i '/g$/d' {}".format(logfile))
    quit()

SCORE = float(argv[2])
DEVIANCE = float(argv[3])
SCR_DIFF = float(argv[4])
DEV_DIFF = float(argv[5])
img_file = str(argv[6])

# Detachment thresholds
SCR_THRES = 1.0
DEV_THRES = 1.0

# Partial Breakage thresholds for DIFF values
BR_SCR_THRES = 0.2
BR_DEV_THRES = 0.2

# Filament run out/clog thresholds
FIL_SCR_THRES = 0.2
FIL_DEV_THRES = 0.2


# This indicates the model has detached from the bed
if SCORE > SCR_THRES and DEVIANCE > DEV_THRES:
    print("Cause: Print detached from bed")
    pause_print()
# This indicates a part of the model has broken off
elif SCR_DIFF > BR_SCR_THRES and DEV_DIFF > BR_DEV_THRES:
    print("Cause: Potential (partial) breakage")
    pause_print()
elif SCORE < FIL_SCR_THRES and DEVIANCE < FIL_DEV_THRES:
    print("Cause: Filament ran out or nozzle/extruder clog")
    pause_print()

else:
    import cv2
    from ml_api.lib.detection_model import load_net, detect

    net_main, meta_main = load_net("./ml_api/model/model.cfg", "./ml_api/model/model.weights", "./ml_api/model/model.meta")
    img = cv2.imread(img_file)
    detection = detect(net_main, meta_main, img, thresh=0.3)
    print(len(detection))
    if len(detection) > 0:
        print("Cause: Spaghetti")
        pause_print()

logfile = dirname(img_file) + '/output.log'
os.system("sed -i '/g$/d' {}".format(logfile))