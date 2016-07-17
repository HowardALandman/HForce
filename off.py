#!/usr/bin/python

import time
import math
import array
from dotstar import Adafruit_DotStar

numpixels = 72 # Number of LEDs in strip

strip   = Adafruit_DotStar(numpixels)           # Use SPI (pins 10=MOSI, 11=SCLK)

strip.begin()           # Initialize pins for output
strip.setBrightness(64) # Limit brightness to ~1/2 duty cycle

# Initialize CA, for now with 1 pixel
cells = array.array('B',(0,)*numpixels)

# Set strip colors and display them
for i in range(numpixels):
	strip.setPixelColor(i, 0x000000)
strip.show()                     # Refresh strip
