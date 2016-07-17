#!/usr/bin/python

# Demo of ColorMap capabilities.
# For now, we only handle static (unchanging in time) ColorMaps,
# but eventually we'd like to have shifting ones as in G-Force.
# As a first step, allow ColorMaps to be read from .png files.
# Normally these would be 256 x 1 x 8-bit RGB.

import array
import numpy
import random
import time
from dotstar import Adafruit_DotStar
from fnmatch import filter
from readColorMaps import readColorMaps

colorMaps = readColorMaps()

numpixels = 72 # Number of LEDs in strip

strip   = Adafruit_DotStar(numpixels)           # Use SPI (pins 10=MOSI, 11=SCLK)
# strip   = Adafruit_DotStar(numpixels, 32000000) # SPI @ ~32 MHz
# strip   = Adafruit_DotStar()                    # SPI, No pixel buffer
# strip   = Adafruit_DotStar(32000000)            # 32 MHz SPI, no pixel buf
# See image-pov.py for explanation of no-pixel-buffer use.
# Append "order='gbr'" to declaration for proper colors w/older DotStar strips)

strip.begin()           # Initialize pins for output
strip.setBrightness(32) # Limit brightness to ~1/8 duty cycle

#m = random.randrange(len(colorMaps))
#n_colors = 256

def sigmoid(x):
	# An S-shaped curve that is 0 for x <= 0 and 1 for x >=1
	# I couldn't find a good one on the web,
	# so build one out of 2 parabolas.
	if (x <= 0):
		return 0.0
	elif (x <= 0.5):
		return 2.0*x*x
	elif (x < 1.0):
		return (1.0 - 2.0*(1.0-x)*(1.0-x))
	else:
		return 1.0

def displayColorMap(cm):
	# Display the colormap on the strip.
	n_colors = int(len(cm)/3)
	for p in range(numpixels):
		# Just truncate for now.
		c = int(p * n_colors // numpixels)
		# Colormap is RGB but strip is GRB
		color = (cm[3*c+1]<<16) | (cm[3*c]<<8) | cm[3*c+2]
		strip.setPixelColor(p, color)
	strip.show()                     # Refresh strip

# Display first ColorMap.
old_m = random.randrange(len(colorMaps))
old_map = numpy.array(colorMaps[old_m][2][0])
displayColorMap(old_map)

cm_FadeTime = 4.0

while True:                              # Loop forever
	time.sleep(1.0)	# Keep displaying the same ColorMap for a while

	# Get a new ColorMap, and transition from the old one to the new one.
	new_m = random.randrange(len(colorMaps))
	new_map = numpy.array(colorMaps[new_m][2][0])
	start = time.time()
	end = start + cm_FadeTime
	# Fade from old to new
	now = time.time()
	while (now < end):
		frac = sigmoid((now - start) / cm_FadeTime)
		map = (numpy.rint(old_map*(1.0-frac) + new_map*frac)).astype(int)
		displayColorMap(map)
		time.sleep(1.0/50)	# ~50 Hz change rate
		now = time.time()
	displayColorMap(new_map)	# Make sure we get 100% there.
	# Prepare for next loop.
	old_m = new_m
	old_map = new_map
