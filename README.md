# 3DPrintSaviour

## What is 3DPrintSaviour?
3DPrintSaviour (3DPS) is a automatic print failure detection system for 3D printers and runs on Raspberry Pi 3 models. It uses Octoprint and Octolapse to get timelapse images, which 3DPS uses to determine if a failure occurred.

## How does it work?
Octolapse generates amazing timelapse images where, from the camera's viewpoint, only the 3D model changes. These images are sent to another Pi (using lsyncd/rsync), where the arrival of a new image (with inotifywait) triggers the Python scripts. By comparing the previous layer image to the current layer image and through the use of OpenCV, a Structured Similarity Index (SSIM) value is calculated, which represents how similar the two images are, with a value of 1 meaning that the images are identical. Due to changes in lighting, this value stays at around 0.97-0.98 during a simple 3D print. When the value goes below 0.95, the system triggers, sending a pause command to Octoprint via the REST API (using Octoclient) and printing out the layer at which it failed.

## Plan and Roadmap
This is a Final Year Project (FYP) at Imperial College London and therefore there are deadlines to meet. Please note that currently I am only testing this system on a modified Original Prusa i3 MK2S and I will not add support for other printers, although doing so should be trivial.

Currently planned are:
* Simple failure detection (Is a model there or not) - TESTING
* Detection by comparing top-down image with 2D gcode (should be more accurate, but timelapses will not be nice) - NOT STARTED

Other features being considered are:
* Email notification upon print failure with attached snapshot
* Conversion to a Octoprint plugin (will require a lot of work due to the size of OpenCV, but may be possible with an external server processing the images...)
* Attempt to put the entire system on the same Pi hosting Octoprint
