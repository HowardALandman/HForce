# HForce
1-D LED strip driver and music visualizer

This is my attempt to build a rich, non-repetitive, music visualizer for a hardware system comprising an Adafruit DotStar LED strip driven by a Raspberry Pi 3. The Pi 3 has much faster serial I/O than the Pi 2, so although all of this code should run on a Pi 2, the performance may not be as good.

Many ideas have been borrowed from other systems.
- WaveWand (1984) was a 1-D oscilloscope I built using TTL chips and a really nice Hewlett-Packard bar graph display with 101 red LEDs in 4 inches.
- Andy O'Meara's G-Force (www.soundspectrum.com) was a shining example of modular design and visual artistry. The partitioning of the system into ColorMaps, FlowFields, WaveShapes, etc. comes from G-Force, as does the idea of gradually fading each of those when changing from one to the next.
- There are also some features in HForce that are things I would *like* to have seen in G-force. These include alternate transition types, strobing, forced symmetry (kaleidoscoping), gain > 1 effects, and cellular automata. Not all of these are implemented yet, and some are implemented only in a separate test program but not yet integrated.


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
