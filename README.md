# 3DPrintSaviour

## What is 3DPrintSaviour?
3DPrintSaviour (3DPS) is a automatic print failure detection system for 3D printers and runs on Raspberry Pi 3 models. It uses Octoprint and Octolapse to get timelapse images, which 3DPS uses to determine if a failure occurred.

## How does it work?
Octolapse generates amazing timelapse images where, from the camera's viewpoint, only the 3D model changes. These images are sent to another Pi (using lsyncd/rsync), where the arrival of a new image (with inotifywait) triggers the Python scripts. By comparing the previous layer image to the current layer image and through the use of OpenCV, a score in the form of a Normalised Root Mean-Squared Error (NRMSE) value is calculated, which represents how similar the two images are, with values over 1 representing a significant deviation. This value stays consistently below 1 after shadow thresholding during a simple 3D print. When the value goes above 1, the system triggers, sending a pause command to Octoprint via the REST API (using Octoclient) and printing out the layer at which it failed in the Pi's terminal.

## Changelog
### 04/04/2018 (3DPS V1)
* Removed (and reset) API keys and URLs. Silly me!
* Refactored Python files to make more sense and be more usable
* Renamed Python files to make more sense and not rely on the score method
* Switched from using Structured Similarity Index (SSIM) to Normalised Root Mean-Squared Error (NRMSE) for the score value
* Changed SSIM threshold to 0.995
* Added background removal by subtracting grayscale image 0 from grayscale images (prev and current) with cv2.absdiff
* Added thresholding to foregound images to remove shadows

### 03/04/2018 (3DPS V1)
* Initial commit to GitHub
* Used SSIM to calculate the score to detect simple print failures (initial SSIM threshold of 0.95)
* Added Readme
* Changed SSIM threshold to 0.973

## Plan and Roadmap
This is a Final Year Project (FYP) at Imperial College London and therefore there are deadlines to meet. Please note that currently I am only testing this system on a modified Original Prusa i3 MK2S and I will not add support for other printers, although doing so should be trivial.

Currently planned are:
* **3DPS V1** Simple failure detection (Is a model there or not) - TESTING
* **3DPS V2** Detection by comparing top-down image with 2D gcode (should be more accurate, but timelapses will not be nice) - NOT STARTED

Other features being considered are:
* Email notification upon print failure with attached snapshot
* Conversion to a Octoprint plugin (will require a lot of work due to the size of OpenCV, but may be possible with an external server processing the images...)
* Attempt to put the entire system on the same Pi hosting Octoprint (probably won't do this, but it may be possible)

## Acknowledgements and References

Many thanks to:

**Dr Peter Cheung** - For giving me the opportunity to work on an awesome and useful project as part of degree.

**Gina Häußge** - [Octoprint](https://octoprint.org/) - The printer control software used here. An amazing project used by many 3D printer owners.

**FormerLurker** - [Octolapse](https://github.com/FormerLurker/Octolapse) - The Octoprint plugin that does amazing, customisable timelapses. Can be added to Octoprint through the Plugin Manager.

**Miro Hrončok** - [Octoclient](https://github.com/hroncok/octoclient) - A Python wrapper for the Octoprint REST API. Easy to use and definitely more readable than manual GET/POST requests.

**Axel Kittenberger** - [lsyncd](https://github.com/axkibe/lsyncd) - Lsyncd (Live Syncing Daemon) is used for syncing the Octolapse timelapse image directory to the Pi hosting the OpenCV code. It's pretty fast too!

**Radu Voicilas** - [inotify-tools](https://github.com/rvoicilas/inotify-tools) - C Library and command line tools that extend inotify's functions. This project uses inotify-wait, which is used as a trigger whenever new files are added to a watched directory. Extremely useful for file-based event handling.

**Stéfan van der Walt, Johannes L. Schönberger, Juan Nunez-Iglesias, François Boulogne, Joshua D. Warner, Neil Yager, Emmanuelle Gouillart, Tony Yu and the scikit-image contributors** - [scikit-image](http://scikit-image.org/) - scikit-image is a Python package for image processing. This project uses it for calculating the score, whether this be SSIM or NRMSE.

**OpenCV team** - [OpenCV](https://opencv.org/) - One of the most important components, OpenCV allows me, with minimal computer vision knowledge, to perform complex operations on images.

Adrian Rosebrock - [OpenCV on Pi](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) + [Image Difference](https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/) - This guy is THE authority on using OpenCV with Python, Raspberry Pis, etc. His tutorials are amazing, informative and very well-written. I used his guides on installing OpenCV for Python on Raspbian Stretch, as well as his Image Difference using OpenCV and Python tutorial. I went from a OpenCV n00b to somewhat understanding OpenCV to the point where I could do some image processing myself. Definitely check out his site!

**Kim Salmi** - [Fall Detection](https://github.com/infr/falldetector-public/blob/master/thesis.md) - This guy is working on a CV solution for improving safety for home care patients, thus taking care of our aging population. His thesis gave me the information needed to improve 3DPS V1, by simply adding the thresholding to remove shadows. Thanks so much, this saved me so much pain and effort and I'm glad I chanced upon your thesis.

Regarding the open-source projects above, I'd also like to thank all of the contributors involved. I understand that such big projects cannot be done on their own and I really appreciate it.  
