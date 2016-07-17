#!/usr/bin/python

# Simple strand test for Adafruit Dot Star RGB LED strip.
# This is a basic diagnostic tool, NOT a graphics demo...helps confirm
# correct wiring and tests each pixel's ability to display red, green
# and blue and to forward data down the line.  By limiting the number
# and color of LEDs, it's reasonably safe to power a couple meters off
# USB.  DON'T try that with other code!

import time
import math
from dotstar import Adafruit_DotStar

numpixels = 72 # Number of LEDs in strip

# Here's how to control the strip from any two GPIO pins:
#datapin   = 23
#clockpin  = 24
#strip     = Adafruit_DotStar(numpixels, datapin, clockpin)

# Alternate ways of declaring strip:
strip   = Adafruit_DotStar(numpixels)           # Use SPI (pins 10=MOSI, 11=SCLK)
# strip   = Adafruit_DotStar(numpixels, 32000000) # SPI @ ~32 MHz
# strip   = Adafruit_DotStar()                    # SPI, No pixel buffer
# strip   = Adafruit_DotStar(32000000)            # 32 MHz SPI, no pixel buf
# See image-pov.py for explanation of no-pixel-buffer use.
# Append "order='gbr'" to declaration for proper colors w/older DotStar strips)

strip.begin()           # Initialize pins for output
strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle

# Runs 10 LEDs at a time along strip, cycling through red, green and blue.
# This requires about 200 mA for all the 'on' pixels + 1 mA per 'off' pixel.

color = 0xFF0000        # 'On' color (starts red)
wave = 0		# radians
dot = 0
freq = 16		# Hertz (cycles per second)
angle_mult = 2*math.pi*freq
mod_period = 1.0	# seconds
start = time.time()

while True:                              # Loop forever

	# rotate color through rainbow
	if (color & 0xFF0000) and not (color & 0x0000FF):
		color = color - 0x010000 # decrement red
		color = color + 0x000100 # increment green
	elif(color & 0x00FF00):
		color = color - 0x000100 # decrement green
		color = color + 0x000001 # increment blue
	elif(color & 0x0000FF):
		color = color - 0x000001 # decrement blue
		color = color + 0x010000 # increment red

	# Turn off old dot
	strip.setPixelColor(dot, 0)

	# Calculate wave based on time
	now = time.time()
	angle = angle_mult * (now - start)
	amplitude = math.cos(now/mod_period)
	wave = amplitude * math.cos(angle)
	#dot = int(math.floor(((wave + 1.0)*(numpixels-1) + 1.0)/2.0))
	#dot = int(((wave + 1.0)*(numpixels-1)/2.0 + 1.0)//2.0 + numpixels/2)
	dot = int(((wave + 1.0)*(numpixels-1) + 1.0)//2.0)

	# Turn on new dot
	strip.setPixelColor(dot, color)
	strip.show()                     # Refresh strip

	#time.sleep(1.0 / 50)             # Pause 20 milliseconds (~50 fps)

