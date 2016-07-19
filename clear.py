#!/usr/bin/python

import time
import math
import array
from dotstar import Adafruit_DotStar

numpixels = 72 # Number of LEDs in strip

strip   = Adafruit_DotStar(numpixels)           # Use SPI (pins 10=MOSI, 11=SCLK)

strip.begin()           # Initialize pins for output
strip.clear()
strip.show()                     # Refresh strip
