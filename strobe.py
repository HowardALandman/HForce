#!/usr/bin/python

# Test the power supply capability to continuously drive all-on full white.
# Set the strip to all white at lowest brightness, and slowly ramp up.

import time
from dotstar import Adafruit_DotStar

WHITE = 0xFFFFFF
MAX_BRIGHTNESS = 255
n_pixels = 72	# Number of LEDs in strip
strip   = Adafruit_DotStar(n_pixels)	# Use SPI (pins 10=MOSI, 11=SCLK)
strip.begin()	# Initialize pins for output
frequency = 12	# Hz
period = 1.0/frequency	# seconds
duty_cycle = 0.125
on_period = duty_cycle * period
off_period = period - on_period

for p in range(n_pixels):
	strip.setPixelColor(p, WHITE)

while True:
	strip.setBrightness(MAX_BRIGHTNESS)
	strip.show()                     # Refresh strip
	time.sleep(on_period)
	strip.setBrightness(0)
	strip.show()                     # Refresh strip
	time.sleep(off_period)


