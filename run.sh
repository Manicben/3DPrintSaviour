#!/bin/sh
DIR="/home/pi/FYP/test_images"

inotifywait -m -r -e moved_to --format '%w%f' "$DIR" | while read f

do
	/home/pi/FYP/ssim2printer.py `/home/pi/FYP/get_ssim.py "$f"`
done
