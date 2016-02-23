#!/usr/bin/env python

import sys
import time
import csv
import os
import subprocess as sp
from os import devnull

# Global variables until we have a config file
freqmin = 151000000
freqmax = 156500000
alarmthresh = 7
powerfftw_path = "/usr/local/bin/rtl_power_fftw"
rtlpower_path = "/usr/local/bin/rtl_power"
fftb = 512
otherargs = "-c"
block_scan_time = 1
baseline_path = "/home/evan/build/baseline_data.dat"
ppm_offset = 56
bline_int_t = "10m"

# Global that we'll keep
dvnll = open(devnull, 'wb')

# Functions
def bline_build(fmin, fmax, bins, b_time, offset):
	# Define and format parameters	
	damnarray = []
	binsize = (fmax - fmin) / bins
	freq = "-f " + str(fmin) + ":" + str(fmax) + ":" + str(binsize)
	ppm = "-p " + str(offset)
	bline_t = "-i " + b_time
	oneshot = "-1"

	print "Defining baseline, this will take some time..."

	rtlpower = sp.Popen([rtlpower_path, freq, oneshot, bline_t, ppm], stdout=sp.PIPE, stderr=dvnll)

	for line in iter(rtlpower.stdout.readline, b""):
		reader = csv.reader(line.split('\n'), delimiter=',')
		for row in reader:
			for element in row:
				if not (':' in element or 'nan' in element or element == time.strftime("%Y-%m-%d")):
					if float(element) < 100: damnarray.append(element)

	return damnarray

# Start your engines...
if __name__ == '__main__':

	# Import settings file here...

	# Parameter formatting
	freqrange = "-f " + str(freqmin) + ":" + str(freqmax)
	fftbins = "-b " + str(fftb)
	bstime = "-t " + str(block_scan_time)
	baseline_arg = "-B " + baseline_path
	ppm = "-p " + str(ppm_offset)

	# Ready, set, GO!
	try:
		print "Starting up at", time.strftime("%H:%M:%S") + "..."
		
		# Check for baseline file
		if not os.path.isfile(baseline_path):
			# Generate said baseline file
			bline = bline_build(freqmin, freqmax, fftb, bline_int_t, ppm_offset)
			for i in bline:
				with open(baseline_path, 'a') as baselinefile: baselinefile.write(i + '\n')

		rpf = sp.Popen([powerfftw_path, freqrange, otherargs, bstime, ppm, baseline_arg], stdout=sp.PIPE, stderr=dvnll, shell=False)

		# Let's see what's going on with rtl_power_fftw
		for line in iter(rpf.stdout.readline, b""):
			# Take out the garbage output
			if '#' in line or not line.strip():
				floats = [0,-999]

			# Convert output to a 2-element array of floats (frequency, strength)
			else:
				floats = map(float, line.split())

			# There be cops nearby!
			if floats[1] >= alarmthresh:
				# Still developing--will provide alert function once the whole noisy frequency issue is solved.
				freq_temp = round(floats[0] /1000000, 3)
				print "At " + time.strftime("%H:%M:%S") + ", a " + str(round(floats[1], 1)) + " dB/Hz signal was detected at " + str(freq_temp) + " MHz."

	except (KeyboardInterrupt, SystemExit): # Press ctrl-c

		rpf.kill()
