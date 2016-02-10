from __future__ import print_function, division
import sys
import numpy as np
from imageio import imread
import cv2
import os
import time

from clickpoints.SendCommands import HasTerminateSignal, CatchTerminateSignal, GetImage, JumpToFrameWait, ReloadMarker
from clickpoints.MarkerLoad import DataFile

df = DataFile()
CatchTerminateSignal()

lk_params = dict(winSize=(8, 8), maxLevel=0, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

start_frame = int(sys.argv[2])

image_current, last_image_id, last_image_frame = GetImage(start_frame)
points = df.GetMarker(image=last_image_id, image_frame=last_image_frame, processed=0)
p0 = np.array([[point.x, point.y] for point in points if point.track_id]).astype(np.float32)
tracking_ids = [point.track_id for point in points if point.track_id]
types = [point.type_id for point in points]

if len(tracking_ids) == 0:
    print("Nothing to track")
    sys.exit(-1)

frame = start_frame
while True:
    image_next, image_id, image_frame = GetImage(frame+1)
    if image_next is None:
        break

    print("Tracking frame number", frame, ",", len(tracking_ids), "tracks")
    p1, st, err = cv2.calcOpticalFlowPyrLK(image_current, image_next, p0, None, **lk_params)

    df.SetMarker(image=image_id, image_frame=image_frame, x=p1[:, 0], y=p1[:, 1], processed=0, type=types, track=tracking_ids)
    df.SetMarker(image=last_image_id, image_frame=last_image_frame, processed=1, type=types, track=tracking_ids)
    ReloadMarker(frame+1)
    JumpToFrameWait(frame+1)

    p0 = p1
    last_image_id = image_id
    last_image_frame = image_frame
    image_current = image_next
    frame += 1

    if HasTerminateSignal():
        print("Terminating Tracking")
        sys.exit(0)
