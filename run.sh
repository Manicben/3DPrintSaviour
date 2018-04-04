#!/bin/sh
# This script runs both Python scripts when a new file is created via lsyncd
# Note that 'moved_to' is used due to the way rsync works

set -x #Used for debugging
DIR="/home/pi/FYP/test_images" #path to your image folder
PRINTCTRL="/home/pi/FYP/printcontrol.py" #path to printcontrol.py
GETSCORE="/home/pi/FYP/get_score.py" #path to get_score.py

inotifywait -m -r -e moved_to --format '%w%f' "$DIR" | while read f

do
	$PRINTCTRL `$GETSCORE "$f"`
done
