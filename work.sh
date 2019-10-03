#!/bin/bash

dir="$1"
echo "Working on $dir"

echo "filtering CAM events"
grep "^CAM," "$dir/log.log" > "$dir/camonly"

echo "starting CAM event analyzer"
./scripts/gen_cam_graphic.py "$dir/camonly" "$dir/cam_graphic.png"

echo "geotagging images"
./scripts/geotag_by_closest_cam.py "$dir/camonly" "$dir/images/"
