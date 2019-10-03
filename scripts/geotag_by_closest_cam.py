#!/usr/bin/python3

# http://ardupilot.org/copter/docs/common-downloading-and-analyzing-data-logs-in-mission-planner.html

import matplotlib.pyplot as plt
import sys
import piexif
import os
import collections
from datetime import datetime
from GPSPhoto import gpsphoto

LEAP_SECONDS = 18
GPS_TO_UNIX_EPOCH_SECONDS = 315964800

#print(gnsscal.gpswd2date(2073, 3.1))

Event = collections.namedtuple('Event', 'time lat lng alt')

camsfilename = sys.argv[1]
imagesdirname = sys.argv[2]

with open(camsfilename) as inpfile:
	lines = inpfile.readlines()
	lines = [line.split(',') for line in lines]

	# remove whitespace around data
	lines = [list(map(str.strip, line)) for line in lines]

events = []
for l in lines:
	sec_since_week = int(l[2]) / 1000
	week = int(l[3])
	sec_since_gps_epoch = week * 7 * 24 * 60 * 60 + sec_since_week
	sec_since_unix_epoch = sec_since_gps_epoch - LEAP_SECONDS + GPS_TO_UNIX_EPOCH_SECONDS
	time = datetime.fromtimestamp(sec_since_unix_epoch)

	lat  = l[4]
	lng  = l[5]
	alt  = l[6] # in cm above ground
	events.append( Event(time, lat, lng, alt) )

#print(events[:3])

# get path to images
imagefnames = [os.path.join(imagesdirname, f) for f in os.listdir(imagesdirname) if os.path.isfile(os.path.join(imagesdirname, f))]
imagefnames.sort()

print(str(len(imagefnames)) + " images")
print(str(len(events)) + " CAM events")

'''
with open(imagefnames[0], 'rb+') as rawimg:
	img = exif.Image(rawimg)
	dt = datetime.strptime(img.datetime, "%Y:%m:%d %H:%M:%S")
	print(events[0].time,dt)
	cam_time_corr = dt - events[0].time
print("diff between CAM event and picture time:", cam_time_corr)
'''

for imgfname, event in zip(imagefnames, events):
	print(imgfname)

	photo = gpsphoto.GPSPhoto(imgfname)
	info = gpsphoto.GPSInfo((float(event.lat), float(event.lng)), alt = int(float(event.alt)))
	photo.modGPSData(info, imgfname)
