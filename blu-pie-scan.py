#!/usr/bin/env python

from subprocess import call


# Let's run this bitch!
if __name__ == '__main__':

	try:

		print "TEMP"

	except (KeyboardInterrupt, SystemExit): # Press ctrl-c

		call(["killall", "-9", "rtl_power_fftw"])
