# BluPi

### Overview

This script emulates the hardware function of the Target BluEye emergency services alert system. The concept is to use a rtl-sdr compatible radio receiver to continuously scan the typical emergency band radio frequencies using `rtl_power_fftw` as a scanning frontend to rtl-sdr, and then filter/process the scan results for potential emergency radio sources.

Hardware support is currently limited to the Raspberry Pi 2 B, though this could feasibly work on many other systems. Recommended base system is the Raspbian Jessie LITE available here: https://www.raspberrypi.org/downloads/raspbian/ It *should* be possible to run this on a RPi1 as it doesn't consume too much processor power, however I haven't tested it yet.

### Dependencies:
	- libfftw3-dev
	- libtclap-dev
	- librtlsdr-dev
	- libusb-1.0-0-dev
	- cmake
	- rtl-sdr (keenerd experimental branch: https://github.com/keenerd/rtl-sdr.git)
	- rtl_power_fftw: https://github.com/AD-Vega/rtl-power-fftw.git
Installing these packages (on a Debian Jessie system) should also install all of their necessary dependencies for a complete install.

### Installation:
Install/build the dependencies, then copy or clone the blupi-scan.py script. Make sure the script copies as an executable or use `chmod +x blupi-scan.py` to make it so.

### Notes:
	- Further documentation will be provided once the project is nearing completion.
	- Run rtl_test -p for a few minutes to find out your receiver's necessary error correciton in PPM.

### TO-DO:
	- Add alert script (GPIO and potentially audio)
	- Add GPS funtionality to allow speed-based alert sensitivity
	- Create RPi2/RPi3 pre-built image (once project is finished, of course)
