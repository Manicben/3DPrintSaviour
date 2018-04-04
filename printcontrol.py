#!/usr/bin/env python

from sys import argv
from octoclient import OctoClient
from api_keys import URL, API_KEY

# Specify URL and API key for Octoprint
if URL is None:
    URL = 'YOUR OCTOPRINT IP ADDRESS'
if API_KEY is None:
    API_KEY = 'YOUR OCTOPRINT API KEY'

# Get SCORE and current layer from get_score.py
SCORE = float(argv[1])
LAYER = argv[2]

# Set Score error threshold
THRES = 1

if SCORE > THRES:
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

