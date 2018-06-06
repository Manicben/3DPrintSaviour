#!/usr/bin/env python

from sys import argv
from octoclient import OctoClient
from api_keys import URL, API_KEY

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


# Specify URL and API key for Octoprint
if URL is None:
    URL = 'YOUR OCTOPRINT IP ADDRESS'
if API_KEY is None:
    API_KEY = 'YOUR OCTOPRINT API KEY'


if argv[2] == 'nan': # Exit if SCORE is NaN, this occurs on the background and first layer
    exit()

# Get SCORE, DEVIANCE and current layer from get_score.py
LAYER = int(argv[1])
SCORE = float(argv[2])
DEVIANCE = float(argv[3])
SCR_DIFF = float(argv[4])
DEV_DIFF = float(argv[5])

# Detachment thresholds
SCR_THRES = 1.2
DEV_THRES = 1.5

# Partial Breakage thresholds for DIFF values
BR_SCR_THRES = 0.1
BR_DEV_THRES = 0.1

# Filament run out/clog thresholds
FIL_SCR_THRES = 0.25
FIL_DEV_THRES = 0.25

# Do nothing if it is the background or first layer
if LAYER < 6:
    quit()
# This indicates a part of the model has broken off
if SCR_DIFF > BR_SCR_THRES and DEV_DIFF > BR_DEV_THRES:
    print("Cause: Potential (partial) breakage")
    pause_print()
# This indicates the model has detached from the bed
elif SCORE > SCR_THRES and DEVIANCE > DEV_THRES:
    print("Cause: Print detached from bed")
    pause_print()
elif SCORE < FIL_SCR_THRES and DEVIANCE < FIL_DEV_THRES:
    print("Cause: Filament ran out or nozzle/extruder clog")
    pause_print()
