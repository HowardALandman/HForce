#!/usr/bin/python

# Test the power supply handling of large current draw transients.
# Set the strip to all white, and strobe it on and off.

import time
from dotstar import Adafruit_DotStar

WHITE = 0xFFFFFF	# 8-bit GRB
MAX_BRIGHTNESS = 255
n_pixels = 72		# Number of LEDs in strip
strip = Adafruit_DotStar(n_pixels) # Use SPI (pins 10=MOSI, 11=SCLK)
strip.begin()		# Initialize pins for output
frequency = 12		# Hz
period = 1.0/frequency	# seconds
duty_cycle = 0.125
on_period = duty_cycle * period
off_period = period - on_period

for p in range(n_pixels):
	strip.setPixelColor(p, WHITE)

while True:
	# Turn strobe on.
	strip.setBrightness(MAX_BRIGHTNESS)
	strip.show()
	time.sleep(on_period)
	# Turn strobe off.
	strip.setBrightness(0)
	strip.show()
	time.sleep(off_period)

# Note that the actual period will be the specified period PLUS compute time.
