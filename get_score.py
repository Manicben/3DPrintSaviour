#!/usr/bin/env python

# import the necessary packages
from skimage.metrics import normalized_root_mse
from sys import argv, exit, stderr
from os.path import dirname
import os
import cv2

# get filenames
fst_file = argv[1]
#fst_file = 'output/11/spaghetti_test_0.15mm_PLA_MK3S_40m000150.jpg'
if fst_file[-4:] != ".jpg":
    exit()

# Set current image and previous image
curr = int(fst_file[-10:-4])
prev = curr - 1

# For the 1st and 2nd images, output 0
# 1st image is used as background image
# 2nd image has no previous image (gives errors as prev is BG)
if curr == 0:
    print("0 nan")
    print("Background Image", file=stderr)
    exit()
if curr == 1:
    print("1 nan")
    print("First Image, no previous images", file=stderr)
    exit()

snd_file = fst_file[:-10] + str(prev).rjust(6, '0') + fst_file[-4:]

bg_file = fst_file[:-10] + '000000.jpg'

# load the two input images and background image
#imageA = cv2.imread(fst_file)
#imageB = cv2.imread(snd_file)
#imageBG = cv2.imread(bg_file)

# convert the images to grayscale
grayA = cv2.imread(fst_file,0)
grayB = cv2.imread(snd_file,0)
grayBG = cv2.imread(bg_file,0)

# crop the images
grayA = grayA[:, 120:520]
grayB = grayB[:, 120:520]
grayBG = grayBG[:, 120:520]

# Remove background and threshold to remove shadow effects
threshold = 20

diffA = cv2.absdiff(grayA, grayBG)
thresA = cv2.threshold(diffA, threshold, 255, cv2.THRESH_BINARY)[1]

diffB = cv2.absdiff(grayB, grayBG)
thresB = cv2.threshold(diffB, threshold, 255, cv2.THRESH_BINARY)[1]

# compute the Normalised Root Mean-Squared Error (NRMSE) between the two
# images
score = normalized_root_mse(thresA, thresB)

# Compare the current image with the image from 5 layers ago
# This is used to check for filament runout or huge deviance
deviance = 1.0
scr_diff = 0.0
dev_diff = 0.0
if curr > 5:
    trd_file = fst_file[:-10] + str(curr-5).rjust(6, '0') + fst_file[-4:]
    #imageC = cv2.imread(trd_file)
    grayC = cv2.imread(trd_file,0)
    grayC = grayC[:, 120:520]
    diffC = cv2.absdiff(grayC, grayBG)
    thresC = cv2.threshold(diffC, threshold, 255, cv2.THRESH_BINARY)[1]
    deviance = normalized_root_mse(thresA, thresC)

    # Calculate difference compared with previous layer score and deviance
    logfile = dirname(fst_file) + '/output.log'
    with open(logfile) as log:
        data = log.readlines()
    prev_layer = data[-1]
    layer,scr,dev,s_diff,d_diff = prev_layer.split(" ")
    scr_diff = abs(score-float(scr))
    dev_diff = abs(deviance-float(dev))

print("{} {} {} {} {}".format(curr,score,deviance,scr_diff,dev_diff))
print(fst_file)
print("Image: {:d}\t Score: {}\t Deviance: {}\tDiffs: {}/{}".format(curr,score,deviance,scr_diff,dev_diff), file=stderr)
