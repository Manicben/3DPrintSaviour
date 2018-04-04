#!/usr/bin/env python

# import the necessary packages
from skimage.measure import compare_nrmse
from sys import argv, exit, stderr
import imutils
import cv2

# get filenames
fst_file = argv[1]
if fst_file[-4:] != ".jpg":
    exit()
num = int(fst_file[-10:-4]) - 1
if num < 0:
    print("1 0")
    print("First image, no previous images", file=stderr)
    exit()
snd_file = fst_file[:-10] + str(num).rjust(6, '0') + fst_file[-4:]

bg_file = fst_file[:-10] + '000000.jpg'

# load the two input images and background image
imageA = cv2.imread(fst_file)
imageB = cv2.imread(snd_file)
imageBG = cv2.imread(bg_file)

# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
grayBG = cv2.cvtColor(imageBG, cv2.COLOR_BGR2GRAY)

# Remove background and threshold to remove shadow effects
threshold = 100

grayA = cv2.absdiff(grayA, grayBG)
grayA = cv2.threshold(grayA, threshold, 255, cv2.THRESH_BINARY)[1]

grayB = cv2.absdiff(grayB, grayBG)
grayB = cv2.threshold(grayB, threshold, 255, cv2.THRESH_BINARY)[1]

# compute the Normalised Root Mean-Squared Error (NRMSE) between the two
# images

score = compare_nrmse(grayA, grayB)

print("{} {}".format(score,num+1))
print("Image: {:d}\t Score: {}".format(num+1,score), file=stderr)

'''
# This part of the code is for using the SSIM instead of NRMSE.
# NRMSE was found to be a much better metric for this application,
# as anything above 1 is considered a print fail. Very handy.

# compute the Structured Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
from scikit.measure import compare_ssim
(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")

print("{} {}".format(score,num+1))
print("Image: {:d}\t NRMSE: {}".format(num+1,score), file=stderr)

# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# loop over the contours
for c in cnts:
    # compute the bounding box of the contour and then draw the
    # bounding box on both input images to represent where the two
    # images differ
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

# show the output images
cv2.imshow("Original", imageA)
cv2.imshow("Modified", imageB)
cv2.imshow("GrayA", grayA)
cv2.imshow("GrayB", grayB)
cv2.imshow("Diff", diff)
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)
'''