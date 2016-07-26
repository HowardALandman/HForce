#!/usr/bin/python

from hf_globals import n_pixels

HoldTime = 43.0
FadeTime = 4.0

# Define Kaleidoscopes.
# Each Kaleidoscope is a list n_pixels long of integers in range(n_pixels).

# Null Kaleidoscope does not change the screen.
ks_Null = range(n_pixels)

# Left half of screen mirrors right half.
righthalf = range(n_pixels//2,n_pixels)
lefthalf = list(righthalf)	# Make copy so we don't reverse righthalf.
lefthalf.reverse()
ks_MirrorRight = lefthalf + righthalf
assert len(ks_MirrorRight) == n_pixels

# Right half of screen mirrors left half.
lefthalf = range(n_pixels//2)
righthalf = list(lefthalf)	# Make copy so we don't reverse lefthalf.
righthalf.reverse()
ks_MirrorLeft = lefthalf + righthalf
assert len(ks_MirrorLeft) == n_pixels

# Two copies of center of screen, second copy flipped to maintain symmetry.
center = range(n_pixels//4,(3*n_pixels)//4)
center2 = list(center)
center2.reverse()
ks_Eyes = center + center2
assert len(ks_Eyes) == n_pixels

maps = [ ks_Null, ks_Null, ks_MirrorRight, ks_MirrorLeft, ks_Eyes ]
names = [ 'Null', 'Null2', 'MirrorRight', 'MirrorLeft', 'Eyes' ]
#for i in range(len(maps)):
#	print names[i], maps[i]
