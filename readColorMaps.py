# For now, we only handle static (unchanging in time) ColorMaps,
# but eventually we'd like to have shifting ones as in G-Force.
# As a first step, allow ColorMaps to be read from .png files.
# Normally these would be 256 x 1 x 8-bit RGB.
# By default we keep them in directory ColorMaps under the app's home.

import os
import png
from fnmatch import filter

def readColorMaps(d=os.path.join(os.getcwd(),"ColorMaps")):
	all_files = []
	all_paths = []
	# Find all .png files in ColorMaps and its subdirectories.
	for (d, dirs, files) in os.walk(d):
		all_files += files
		for f in files:
			all_paths += [os.path.join(d,f)]
	png_files = filter(all_files, '*.png')
	png_paths = filter(all_paths, '*.png')
	colorMaps = []
	colorMapNames = []
	for p in png_paths:
		colorMaps += [ png.Reader(filename=p).asRGB() ]
		colorMapNames += [ os.path.splitext(os.path.basename(p))[0] ]
	return colorMaps, colorMapNames
