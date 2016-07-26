#!/usr/bin/python

# Test the power supply capability to continuously drive all-on full white.
# Set the strip to all white at lowest brightness, and slowly ramp up.

import time
from dotstar import Adafruit_DotStar

WHITE = 0xFFFFFF
n_pixels = 72	# Number of LEDs in strip
strip   = Adafruit_DotStar(n_pixels)	# Use SPI (pins 10=MOSI, 11=SCLK)
strip.begin()	# Initialize pins for output

# Open log file.
f = open('powerlog.txt', 'w')
f.write("Brightness\tVoltage\n")

for p in range(n_pixels):
	strip.setPixelColor(p, WHITE)

for b in range(256):
	#print b
	# Set the brightness.
	strip.setBrightness(b)
	strip.show()                     # Refresh strip
	# Prompt user for data entry.
	answer = raw_input(str(b)+' ')
	# Log it.
	f.write(str(b)+"\t"+answer+"\n")
	# Wait a fraction of a second to help ensure that the write completes,
	# in case the next brightness level crashes the system.
	time.sleep(0.1)

f.close()
