#!/usr/bin/env python

import sys
import subprocess as sp
import shlex
from time import sleep

# Global variables until we have a config file
fmin = 151000000
fmax = 156500000
alarmthresh = -10
powerfftw_path = "/usr/local/bin/rtl_power_fftw"
fftbins = 512
otherargs = "-c"

# Parameter formatting
frange = str(fmin) + ":" + str(fmax)
frange = "-f " + frange
fftbins = "-b " + str(fftbins)

# Let's run this bitch!
if __name__ == '__main__':
	
	floats = []

	try:
		print "Starting up..."
		
		# Insert baseline file generation subroutine here once main script is completed

		rtlscan = sp.Popen([powerfftw_path, frange, fftbins, otherargs], stdout=sp.PIPE)

		lines_iterator = iter(rtlscan.stdout.readline, b"")
		for line in lines_iterator:

			floats = []
			if '#' in line:
				floats = [0,-99]
			else:
				floats = map(float, line.split())


			if len(floats) > 1:
				if floats[1] >= alarmthresh:
					print floats

	except (KeyboardInterrupt, SystemExit): # Press ctrl-c

		rtlscan.kill()
