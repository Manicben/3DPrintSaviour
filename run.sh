#!/bin/sh
DIR="/home/pi/FYP/test_images"

inotifywait -m -r -e moved_to --format '%w%f' "$DIR" | while read f

do
	/home/pi/FYP/printcontrol.py `/hoce/pi/FYP/get_score.py "$f"`
done
