#!/usr/bin/env python

import sys
import time
import os
import subprocess as sp
from os import devnull
from collections import deque
from math import sqrt

# Global variables until we have a config file
freqmin = 854000000 # DO NOT CHANGE
freqmax = 860000000 # DO NOT CHANGE
sensitivity = 70
sysdamping = 10
freqdamping = 30
powerfftw_path = "/usr/local/bin/rtl_power_fftw"
baseline_path = "baseline_data.dat"
totalbins = 960 * 3 # DO NOT CHANGE
ppm_offset = 56


# Global that we'll keep
dvnll = open(devnull, 'wb')

# Functions
def average(p): return sum(p) / float(len(p))

def variance(p): return map(lambda x: (x - average(p))**2, p)

def std_dev(p): return sqrt(average(variance(p)))

def alert(p):
	# Still developing...need to provide true alert functionality

	freq_temp = round(p[0] /1000000, 4)
	print "At " + time.strftime("%H:%M:%S") + ", a " + str(round(p[1], 1)) + " dB/Hz signal was detected at " + str(freq_temp) + " MHz."


# Start your engines...
if __name__ == '__main__':

	# Import settings file here...

	# Parameter formatting
	freqrange = "-f " + str(freqmin) + ":" + str(freqmax)

	fftb = totalbins / 3 # NEED TO DEVELOP

	fftbins = "-b " + str(fftb)
	ppm = "-p " + str(ppm_offset)
	otherargs = "-c"
	rolling = []
	rolling_avg = deque([])
	sweep = deque([])
	i = 0
	stddev = 100
	baseline_file = "-B " + str(baseline_path)

	# Ready, set, GO!
	try:
		print "Starting up at", time.strftime("%H:%M:%S") + "..."
		
		# Check for baseline file
		#if not os.path.isfile(baseline_path):
		#	# Generate said baseline file
		#	stddev = 10 # THIS IS MEANINGLESS

		#NOTE: Minus bstime and baseline_arg (above)
		rpf = sp.Popen([powerfftw_path, freqrange, otherargs, ppm, fftbins, baseline_file], stdout=sp.PIPE, stderr=dvnll, shell=False)

		# Let's see what's going on with rtl_power_fftw
		for line in iter(rpf.stdout.readline, b""):

			# Ignore garbage output
			if not ('#' in line or not line.strip()):

				floats = map(float, line.split())

				# Create 2D array if it isn't already defined
				if len(rolling) < totalbins: rolling.append(deque([]))

				rolling[i].append(floats[1])
				sweep.append(floats[1])

				# Let's start filtering...
				if len(rolling[i]) >= freqdamping:
					rolling[i].popleft()
					alarmthresh = average(rolling[i]) + stddev / sensitivity * 20000

					#if i == 0: print floats[1], alarmthresh - floats[1]

					# There be coppers!
					if floats[1] > alarmthresh:

						alert(floats)

				# Maintain sweep length at the total number of samples
				if len(sweep) > totalbins: sweep.popleft()

				# Increment or reset indexer (i)
				if i < totalbins - 1: i = i + 1
				else: 
					i = 0

					# Maintain rolling_avg
					rolling_avg.append(average(sweep))

					if len(rolling_avg) > sysdamping: 
						rolling_avg.popleft()
						stddev = std_dev(rolling_avg)


	except (KeyboardInterrupt, SystemExit): # Press ctrl-c

		rpf.kill()
		print "\n", "Buh-bye"
