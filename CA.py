#!/usr/bin/python

import time
import math
import array
from dotstar import Adafruit_DotStar

numpixels = 72 # Number of LEDs in strip
fps = 8	# Nominal target Frames Per Second
# For POV aaplications, need 500+ FPS to get squarish pixels
#fps = 1024	# Nominal target Frames Per Second

strip   = Adafruit_DotStar(numpixels)           # Use SPI (pins 10=MOSI, 11=SCLK)

strip.begin()           # Initialize pins for output
strip.setBrightness(32) # Limit brightness to ~1/4 duty cycle

# 3-color totalistic cellular automaton
# colors are 0, 1, 2 (we usually show 0 as black)
colors = (0x000000, 0xFF0000, 0x007F7F)
ca = [0,1,2,1,0,0,1]	# code 777 CA
# see http://mathworld.wolfram.com/TotalisticCellularAutomaton.html

# Initialize CA, for now with 1 pixel
cells = array.array('B',(0,)*numpixels)
cells[int(numpixels/2)] = 2
sum = array.array('B',(0,)*numpixels)

while True:                              # Loop forever

	# Set strip colors and display them
	for i in range(numpixels):
		strip.setPixelColor(i, colors[cells[i]])
	strip.show()                     # Refresh strip

	# Update CA
	for i in range(numpixels):
		# Sum up cell and its neighbors (with wraparound)
		sum[i] = cells[(i+numpixels-1)%numpixels] + cells[i] + cells[(i+1)%numpixels]
	for i in range(numpixels):
		cells[i] = ca[sum[i]]
	
	time.sleep(1.0 / fps)
