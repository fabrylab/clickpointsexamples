from __future__ import print_function, division
import sys
import numpy as np
from imageio import imread
import cv2

from clickpoints.SendCommands import JumpToFrame, GetImageName, GetMarkerName, HasTerminateSignal, CatchTerminateSignal
from clickpoints.MarkerLoad import LoadLogIDindexed, SaveLog

CatchTerminateSignal()

lk_params = dict(winSize=(8, 8), maxLevel=0, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

start_frame = int(sys.argv[2])

points, types = LoadLogIDindexed(GetMarkerName(start_frame))
image_current = imread(GetImageName(start_frame))
tracking_ids = [id for id in points if not points[id]["processed"]]
if len(tracking_ids) == 0:
    print("Nothing to track")
    sys.exit(-1)

for frame in range(start_frame, start_frame+800):
    next_image = GetImageName(frame+1)
    if next_image == "":
        print("Finished")
        break
    image_next = imread(GetImageName(frame+1))
    p0 = np.array([[points[id]["x"], points[id]["y"]] for id in tracking_ids]).astype(np.float32)
    print("Tracking frame number", frame)
    p1, st, err = cv2.calcOpticalFlowPyrLK(image_current, image_next, p0, None, **lk_params)
    points2 = {}
    for index, id in enumerate(tracking_ids):
        points2[id] = points[id].copy()
        points2[id]["x"] = p1[index, 0]
        points2[id]["y"] = p1[index, 1]
        points2[id]["processed"] = 0
        points[id]["processed"] = 1
    try:
        points_new, types = LoadLogIDindexed(GetMarkerName(frame+1))
    except:
        points_new = {}
    points_new.update(points2)
    SaveLog(GetMarkerName(frame+1), points_new, types)
    SaveLog(GetMarkerName(frame), points, types)
    JumpToFrame(frame+1)

    points = points_new
    image_current = image_next
    if HasTerminateSignal():
        print("Terminating Tracking")
        sys.exit(0)

