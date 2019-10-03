#!/usr/bin/python3

import matplotlib.pyplot as plt
import sys

inpfilename = sys.argv[1]

with open(inpfilename) as inpfile:
	lines = inpfile.readlines()
	lines = [line.split(',') for line in lines]

	# remove whitespace around data
	lines = [list(map(str.strip, line)) for line in lines]

diffs = [] # in seconds
for l1, l2 in zip(lines, lines[1:]):
	t1, t2 = int(l1[2]), int(l2[2])
	diffs.append( (t2 - t1) / 1000)

plt.plot(diffs)
plt.savefig(sys.argv[2])
