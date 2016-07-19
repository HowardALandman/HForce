#!/usr/bin/python

# H-Force 1: A 1-D LED array driver
# Borrowing and adapting some ideas from G-Force,
# as well as cinematic techniques and a bit of pure math.

import alsaaudio, audioop	# for microphone input
import array
import numpy
import random
import time
from dotstar import Adafruit_DotStar
from readColorMaps import readColorMaps

# Initialize USB microphone.
# Borrowing/modifying code from CShadowRun
# (http://ubuntuforums.org/showthread.php?t=500337)
#
# Open the device in nonblocking capture mode.
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
#
# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
# NOTE: A Soundsnake may be locked to CD frequency (44 KHz).  Not sure
# what happens when you try to change that, but this code seems to work.
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
#
# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames, each frame being 2 bytes long.
# This means that the reads below will return either 256 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode, but unlikely because we are doing a lot of other work between calls.
inp.setperiodsize(64)

# Initialize LED strip.
n_pixels = 72 # Number of LEDs in strip
strip   = Adafruit_DotStar(n_pixels)	# Use SPI (pins 10=MOSI, 11=SCLK)
strip.begin()           # Initialize pins for output
MAX_BRIGHTNESS = 64	# Limit brightness to ~1/4 duty cycle
strip.setBrightness(MAX_BRIGHTNESS)

# Read ColorMaps from files.
n_colors = 256	# length of static color maps
colorMaps, colorMapNames = readColorMaps()
cm_HoldTime = 25.0
cm_FadeTime = 4.0
# Choose first ColorMaps.
cm_old_n = random.randrange(len(colorMaps))
cm_old_map = numpy.array(colorMaps[cm_old_n][2][0])
cm_new_n = random.randrange(len(colorMaps))
cm_new_map = numpy.array(colorMaps[cm_new_n][2][0])
print "cm = ", colorMapNames[cm_old_n], "->", colorMapNames[cm_new_n]
# Set up timers for transition.
cm_fade_start = time.time() + cm_HoldTime
cm_fade_end = cm_fade_start + cm_FadeTime

# For now, hard-code a few FlowFields.
# Nowhere: Each pixel points to itself as source, so there is no motion.
ff_Nowhere  = [ 1.0*i for i in range(n_pixels) ]
#print "ff_Nowhere =", ff_Nowhere
# Expand: source is inward so trails are outward.
zoom = 1.0/n_pixels
center = (n_pixels - 1.0) / 2.0
ff_Expand   = [ (zoom*center + (1.0-zoom)*i) for i in range(n_pixels) ]
#print "ff_Expand =", ff_Expand
# Contract: source is outward so trails are inward.
ff_Contract = [ ((1.0+zoom)*i - zoom*center) for i in range(n_pixels) ]
#print "ff_Contract =", ff_Contract
# Flip: Reverse the pixels (left becomes right)
ff_Flip  = [ ((n_pixels-1.0) - i) for i in range(n_pixels) ]
#print "ff_Flip =", ff_Flip
# TentMap: a simple piecewise-linear chaotic system
ff_TentMap  = [ ((n_pixels-1.0) - 2*abs(i-center)) for i in range(n_pixels) ]
#print "ff_TentMap =", ff_TentMap
# Left: Source is to right so pixels move left. Wraps around.
ff_Left  = [ 1.0*((i+1)%n_pixels) for i in range(n_pixels) ]
#print "ff_Left =", ff_Left
# Right: Source is to left so pixels move right. Wraps around.
ff_Right  = [ 1.0*((i + n_pixels -1) % n_pixels) for i in range(n_pixels) ]
#print "ff_Right =", ff_Right
flowFields = [ ff_Nowhere, ff_Expand, ff_Contract, ff_Flip, ff_TentMap, ff_Left, ff_Right ]
flowFieldNames = [ 'Nowhere', 'Expand', 'Contract', 'Flip', 'TentMap', 'Left', 'Right' ]
ff_HoldTime = 25.0
ff_FadeTime = 6.0
# Choose first FlowFields.
ff_old_n = random.randrange(len(flowFields))
ff_old_flow = flowFields[ff_old_n]
ff_new_n = random.randrange(len(flowFields))
ff_new_flow = flowFields[ff_new_n]
print "ff = ", flowFieldNames[ff_old_n], "->", flowFieldNames[ff_new_n]
# Set up timers for transition.
ff_fade_start = time.time() + ff_HoldTime
ff_fade_end = ff_fade_start + ff_FadeTime

# Initial screen is dark.
screen = [ 0.0 for i in range(n_pixels) ]

def ff_interp(s,f,i):
	# NOTE: This may not handle the very edges perfectly yet.
	# Needs more thought.
	ff_from = f[i]
	if ((ff_from < 0.0) or (ff_from >= n_pixels)):
		# We are pointing off the screen. Return "black".
		return 0.0
	from_int = numpy.floor(ff_from)
	lower = int(from_int)
	assert lower >= 0
	upper = lower + 1
	# If we're right at upper edge ...
	if upper >= n_pixels:
		return s[n_pixels-1]
	# Return interpolated value.
	from_frac = ff_from - from_int
	return from_frac*s[upper] + (1.0-from_frac)*s[lower]

def cm_interp(cmap,x):
	# Interpolate colors betweenn the points of a ColorMap.
	if (x <= 0.0):
		c = (int(cmap[0]), int(cmap[1]), int(cmap[2]))
	elif (x >= n_pixels-2):
		c = (int(cmap[-3]), int(cmap[-2]), int(cmap[-1]))
	else:
		from_int = numpy.floor(x)
		lower = 3*int(from_int)
		assert lower >= 0
		upper = lower + 3
		assert upper <= 3*(n_pixels-1)
		assert upper+2 < len(cmap), "upper+2 (%d) >= len(cmap) (%d)" % (upper+2, len(cmap))
		# Return interpolated value.
		from_frac = x - from_int
		c = (int(numpy.rint(from_frac*cmap[upper] + (1.0-from_frac)*cmap[lower])), \
			int(numpy.rint(from_frac*cmap[upper+1] + (1.0-from_frac)*cmap[lower+1])), \
			int(numpy.rint(from_frac*cmap[upper+2] + (1.0-from_frac)*cmap[lower+2])))

	# Return packed color value for the strip.
	# Colormaps are RGB but strip is GRB, thus the 1,0,2 order.
	return ((c[1]<<16) | (c[0]<<8) | c[2])

# Initial position and direction for Larson scanner WaveShape
ws_Larson_p = n_pixels//2
ws_Larson_dir = 1
# What fraction of the strip should we scan
ws_Larson_min = n_pixels//4
ws_Larson_max = 3*n_pixels//4

# Initialize oscilloscope.
osc_pixel = n_pixels//2
osc_pixel_old = osc_pixel
OSC_BOUND = 128
osc_max = OSC_BOUND	# semi-reasonable initial expectation
osc_min = -OSC_BOUND	# semi-reasonable initial expectation

# Target frame rate
frameRate = 50		# Hz
period = 1.0/frameRate	# Seconds

while True:                              # Loop forever
	now = time.time()
	target_time = now + period

	# Transmit previously-computed colors to strip.
	strip.show()

	# Decide which FlowField to apply.
	if (now < ff_fade_start):
		# We're just doing one (old) FlowField.
		flow = ff_old_flow
	elif (now < ff_fade_end):
		# We're transitioning between two FLowFields.
		ff_frac = (now - ff_fade_start) / ff_FadeTime
		flow = [ (ff_new_flow[i]*ff_frac + ff_old_flow[i]*(1.0-ff_frac)) for i in range(n_pixels) ]
	else:
		flow = ff_new_flow
		ff_old_n = ff_new_n
		ff_old_flow = ff_new_flow
		ff_new_n = random.randrange(len(flowFields))
		ff_new_flow = flowFields[ff_new_n]
		ff_fade_start = now + ff_HoldTime
		ff_fade_end = ff_fade_start + ff_FadeTime
		print "ff = ", flowFieldNames[ff_old_n], ", \
			next = ", flowFieldNames[ff_new_n]

	# Apply the FlowField.
	# Interpolate pixel grey values.
	interp_screen = [ ff_interp(screen,flow,i) for i in range(n_pixels) ]

	# Decay values towards 0.0.
	screen = [ x*9/10 for x in interp_screen ]
	
	# Compute WaveShape.
	# Note that a WaveShape must return an entire screen
	# because it may draw in more than one pixel.
	#
	# For now, just one hardwired WaveShape while we debug everything else.
	# Initialize WaveShape to all empty
	wave = [ 0.0 for i in range(n_pixels) ]
#	# "Larson scanner"
#	assert ws_Larson_p >= 0
#	assert ws_Larson_p < n_pixels
#	wave[ws_Larson_p] = 1.0*(n_pixels-1)
#	if ws_Larson_p >= ws_Larson_max:
#		ws_Larson_dir = -1
#		ws_Larson_p = ws_Larson_max - 1
#	elif ws_Larson_p <= ws_Larson_min:
#		ws_Larson_dir = 1
#		ws_Larson_p = ws_Larson_min + 1
#	else:
#		ws_Larson_p += ws_Larson_dir
	# Oscilloscope
	l,data = inp.read()	# Read data from microphone
	#print l, len(data)	# gets 170 340 no matter settings!?
	if l>0:
		osc = audioop.avg(data,2)
		# Note that average filters out high frequencies,
		# so this will only respond to bass.
		if osc > osc_max:
			osc_max = osc
		if osc < osc_min:
			osc_min = osc
		#osc_pixel = int(n_pixels*(osc-osc_min)/(1+osc_max-osc_min))
		osc_pixel = int(n_pixels*(osc-osc_min)/(1+osc_max-osc_min))//2 + n_pixels//4
		#print osc_min, osc_max, osc, osc_pixel
		# Clip to screen bounds.
		osc_pixel = max(0,min(n_pixels-1,osc_pixel))
		# Gradually have the max and min bounds decay in
		# so that one loud spike doesn't permanently mute the wave.
		# Also try to keep the wave roughly centered.
		if (osc_pixel < (n_pixels//2)):
			#osc_max = max(OSC_BOUND,osc_max-2)
			osc_max = max(osc_min+1,osc_max-2)
		else:
			#osc_min =  min(-OSC_BOUND,osc_min+2)
			osc_min =  min(osc_max-1,osc_min+2)
	for i in range(osc_pixel_old,osc_pixel):
		wave[i] = 1.0*(n_pixels-1)
	wave[osc_pixel] = 1.0*(n_pixels-1)
	osc_pixel_old = osc_pixel
	# Apply WaveShape.
	for i in range(n_pixels):
		screen[i] = max(screen[i],wave[i])
	# Yes, it would be more efficient (but less flexible) to draw the
	# wave directly into screen.

	# Finally use ColorMap to convert grey screen to RGB color.
	# Decide which ColorMap to apply.
	# Note that we shouldn't use "map" as a variable name
	# since map() is a built in function. Use "cm_map" instead.
	if (now < cm_fade_start):
		# We're just doing one (old) ColorMap.
		cm_map = cm_old_map
	elif (now < cm_fade_end):
		# We're transitioning between two ColorMap.
		cm_frac = (now - cm_fade_start) / cm_FadeTime
		#print "cm_old_map[0] = ", cm_old_map[0]
		#print "cm_new_map[0] = ", cm_new_map[0]
		#cm_map = [ int(cm_frac*(cm_new_map[i]) + (1.0-cm_frac)*(cm_old_map[i])) for i in range(n_colors) ]
		cm_map = numpy.rint(cm_old_map*(1.0-cm_frac) + cm_new_map*cm_frac).astype(int)
	else:
		# Time to switch completely to the new ColorMap
		cm_map = cm_new_map
		cm_old_n = cm_new_n
		cm_old_map = cm_new_map
		cm_new_n = random.randrange(len(colorMaps))
		cm_new_map = numpy.array(colorMaps[cm_new_n][2][0])
		cm_fade_start = now + cm_HoldTime
		cm_fade_end = cm_fade_start + cm_FadeTime
		print "cm = ", colorMapNames[cm_old_n], ", \
			next = ", colorMapNames[cm_new_n]
	# Apply the ColorMap.
	for p in range(n_pixels):
		strip.setPixelColor(p, cm_interp(cm_map,screen[p]))
	# Fade to black if volume is low.
	strip.setBrightness(min(MAX_BRIGHTNESS,(osc_max-osc_min)//2))

	# Sleep if we finished with time to spare.
	delta = target_time - time.time()
	if (delta > 0.0):
		time.sleep(delta)
	else:
		print delta
