#!/usr/bin/env python

from sys import argv
from octoclient import OctoClient
from api_keys import URL, API_KEY

# Specify URL and API key for Octoprint
if URL is None:
    URL = 'YOUR OCTOPRINT IP ADDRESS'
if API_KEY is None:
    API_KEY = 'YOUR OCTOPRINT API KEY'

# Get SCORE, DEVIANCE and current layer from get_score.py
if SCORE == 'nan': # Exit if SCORE is NaN, this occus on first layer
    exit()
LAYER = argv[1]
SCORE = float(argv[2])
DEVIANCE = float(argv[3])

# Set SCORE error threshold
THRES = 1.0

# Set SCORE and DEVIANCE thresholds
SCR_THRES = 0.7
DEV_THRES = 0.9


# This indicates a part of the model has broken off
if SCORE > SCR_THRES and DEVIANCE > DEV_THRES:
    pause_print()
# This indicates the model has detached from the bed
elif SCORE > THRES:
    pause_print()


# Pause the printer
def pause_print():
    try:
        client = OctoClient(url=URL, apikey=API_KEY)
        flags = client.printer()['state']['flags']
        if flags['printing']:
            client.pause()
            print("Print paused.")
            print("Layer: " + LAYER)
        elif flags['paused'] or flags['pausing']:
            print("Print already paused.")
        else:
            print("Print cancelled or error occurred.")
    except Exception as e:
        print(e)

