from __future__ import print_function, division
import sys
import numpy as np
from scipy.misc import imread
import cv2

from clickpoints.SendCommands import JumpFrames, GetImageName, GetMarkerName
from clickpoints.MarkerLoad import LoadLog, SaveLog

lk_params = dict(winSize=(8, 8), maxLevel=0, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

start_frame = int(sys.argv[2])

for frame in range(start_frame, start_frame+800):
    points, types = LoadLog(GetMarkerName(frame))
    p0 = np.array([[point["x"], point["y"]] for point in points]).astype(np.float32)
    try:
        old_gray = imread(GetImageName(frame))
        frame_gray = imread(GetImageName(frame+1))
    except IOError:
        print("Finished")
        break
    print("Tracking frame number", frame)
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    point2 = points[:]
    for i in range(p1.shape[0]):
        point2[i]["x"] = p1[i, 0]
        point2[i]["y"] = p1[i, 1]
    SaveLog(GetMarkerName(frame+1), point2, types)
    JumpFrames(1)
