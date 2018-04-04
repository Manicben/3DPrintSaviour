#!/usr/bin/env python

from sys import argv
from octoclient import OctoClient

# Specify URL and API key for Octoprint
URL = 'http://146.169.145.97/'
API_KEY = '91B5F50805DE468799850E3BCF804CE6'

# Get SCORE and current layer from get_score.py
SCORE = float(argv[1])
LAYER = argv[2]

# Set Score error threshold
THRES = 1

if SSIM > THRES:
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
