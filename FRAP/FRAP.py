from __future__ import division, print_function
import numpy as np
import sys
import matplotlib.pyplot as plt

import clickpoints

# Connect to database
start_frame, database, port = clickpoints.GetCommandLineArgs()
db = clickpoints.DataFile(database)
com = clickpoints.Commands(port)

# Check if the marker types are present
if not db.GetType("FRAP_bleach"):
    db.AddType("FRAP_bleach", [0, 255, 0], db.TYPE_Rect)
    com.ReloadTypes()
if not db.GetType("FRAP_background"):
    db.AddType("FRAP_background", [0, 128, 0], db.TYPE_Rect)
    com.ReloadTypes()

# try to load marker
rects_bleach = db.GetRectangles(type_name="FRAP_bleach")
rects_background = db.GetRectangles(type_name="FRAP_background")

# check if we have at least one bleach region
if len(rects_bleach) < 1:
    print("ERROR: no rectangle selected.\nPlease mark a rectangle with type 'FRAP_bleach'.")
    sys.exit(-1)

# get all the images
images = db.GetImages()

# define empty lists
bleach = []  # bleach should store for each bleach region the mean intensity over time
background = []  # background should store the mean over all background regions over time
# start iteration
for image in images:
    # go through all bleach regions and extract the mean intensity
    bleach_values = []
    for bleach_rect in rects_bleach:
        bleach_values.append(np.mean(image.data[bleach_rect.y1:bleach_rect.y2, bleach_rect.x1:bleach_rect.x2]))
    bleach.append(bleach_values)
    # go through all the background regions and sum up the mean intensity
    background_value = 0
    for background_rect in rects_background:
        background_value += np.mean(image.data[background_rect.y1:background_rect.y2, background_rect.x1:background_rect.x2])
    background.append(background_value/len(rects_background))

# subtract the mean background from all bleach intensities
bleach = np.array(bleach).T - np.array(background)

# plot each bleach intensity over time
for b in bleach:
    plt.plot(b)
# some labels
plt.xlabel("frame number")
plt.ylabel("intensity")
# show the plot
plt.show()
