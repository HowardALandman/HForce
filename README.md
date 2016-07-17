# HForce
1-D LED strip driver and music visualizer

First functional release:
HF1.py			- main program
readColorMaps.py	- subroutine to looad all the ColorMaps
			  NOTE: ColorMaps not included due to possible
			  copyright issues.  Each (static) ColorMap is
			  a 256x1x8-bit .png file.
CA.py			- A simple 3-state cellular automaton.
ColorMap_test.py	- Tests ColorMaps by displaying each one on the strip.
dotstar.c		- Low-level code from Adafruit to drive the DotStar.
off.py			- Sets all pixels to black, i.e. turns off the strip.
power_test.py		- Sets all pixels to full white and slowly ramps up
			  the brightness, to test how hard we can drive the
			  DotStar without overloading our power supply.  On
			  my system, it was able to go all the way to 255
			  without crashing. The red power light on the RP3
			  went out at some point, but everything kept running.

strobe.py		- Strobe light: max brightness flash followed by black,
			  partly to test effect of large power transients.
WaveWand.py		- Sine wave test for a 1-D POV oscilloscope.
