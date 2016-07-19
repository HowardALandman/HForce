#!/usr/bin/python

# Test the power supply capability to continuously drive all-on full white.
# Set the strip to all white at lowest brightness, and slowly ramp up.

import time
from dotstar import Adafruit_DotStar

WHITE = 0xFFFFFF
n_pixels = 72	# Number of LEDs in strip
strip   = Adafruit_DotStar(n_pixels)	# Use SPI (pins 10=MOSI, 11=SCLK)
strip.begin()	# Initialize pins for output

for p in range(n_pixels):
	strip.setPixelColor(p, WHITE)

for b in range(256):
	#print b
	strip.setBrightness(b)
	strip.show()                     # Refresh strip
	answer = raw_input(str(b)+' ')
	#time.sleep(1.0)


