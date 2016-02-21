#!/usr/bin/env python

import sys
import subprocess
from time import sleep

# Global variables until we have a config file
fmin = 151000000
fmax = 156500000

# Parameter formatting
frange = str(fmin) + ":" + str(fmax)
frange = "-f " + frange


# Let's run this bitch!
if __name__ == '__main__':

	try:

		print "Starting up..."
		
		# Insert baseline file generation subroutine here once main script is completed

		rtlscan = subprocess.Popen(['/usr/local/bin/rtl_power_fftw', '-b 512', frange, '-c'], stdout=subprocess.PIPE)

		lines_iterator = iter(rtlscan.stdout.readline, b"")
		for line in lines_iterator:
			print line

	except (KeyboardInterrupt, SystemExit): # Press ctrl-c

		rtlscan.kill()
