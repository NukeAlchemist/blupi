### Blu Pie ###

This software basically emulates the hardware function of the Target Blu Eye. The concept is to use a rtl-sdr compatible radio receiver to continuously scan the typical emergency band radio frequencies using rtl_power_fftw as a scanning frontend to rtl-sdr, and then filter/process the scan results for potential emergency radio sources.

Dependencies:
	- rtl-sdr
	- libfftw3-dev
	- libtclap-dev
	- librtlsdr-dev
	- libusb-1.0-0-dev
	- cmake
	- rtl_power_fftw: https://github.com/AD-Vega/rtl-power-fftw.git

Further documentation will be provided once the project is at least nearing completion.

