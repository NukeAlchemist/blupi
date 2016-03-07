#!/usr/bin/env python

import sys
import time
import os
import subprocess as sp
from os import devnull
from collections import deque

# Global variables until we have a config file
freqmin = 855000000
freqmax = 860000000
sensitivity = 35
powerfftw_path = "/usr/local/bin/rtl_power_fftw"
fftb = 800
otherargs = "-c"
block_scan_time = .75
ppm_offset = 56

# Global that we'll keep
dvnll = open(devnull, 'wb')

# Functions
def average(s): return sum(s) / float(len(s))

# Start your engines...
if __name__ == '__main__':

	# Import settings file here...

	# Parameter formatting
	freqrange = "-f " + str(freqmin) + ":" + str(freqmax)
	fftbins = "-b " + str(fftb)
	#bstime = "-t " + str(block_scan_time)
	bstime = ""
	ppm = "-p " + str(ppm_offset)
	rolling = deque([])

	# Ready, set, GO!
	try:
		print "Starting up at", time.strftime("%H:%M:%S") + "..."
		
		rpf = sp.Popen([powerfftw_path, freqrange, bstime, otherargs, ppm], stdout=sp.PIPE, stderr=dvnll, shell=False)
		#NOTE: Minus bstime and baseline_arg (above)

		# Let's see what's going on with rtl_power_fftw
		for line in iter(rpf.stdout.readline, b""):
			# Take out the garbage output
			if '#' in line or not line.strip():
				floats = [0,-999]

			# Convert output to a 2-element array of floats (frequency, strength) and maintain rolling/roling_avg
			else:
				floats = map(float, line.split())
				rolling.append(floats[1])

				# Let's start filtering...
				if len(rolling) >= 2500:
					rolling.popleft()
					rolling_avg = average(rolling)
					alarmthresh = rolling_avg + sensitivity

					# There be coppers!
					if floats[1] > alarmthresh:

						# Still developing...need to provide true alert functionality
						freq_temp = round(floats[0] /1000000, 4)
						print "At " + time.strftime("%H:%M:%S") + ", a " + str(round(floats[1], 1)) + " dB/Hz signal was detected at " + str(freq_temp) + " MHz."

	except (KeyboardInterrupt, SystemExit): # Press ctrl-c

		rpf.kill()
		print "\n", "Buh-bye"
