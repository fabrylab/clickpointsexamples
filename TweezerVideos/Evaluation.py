from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt

# connect to ClickPoints database
# database filename is supplied as command line argument when started from ClickPoints
import clickpoints
db = clickpoints.DataFile()

# get all tracks
tracks = db.GetTracks()

# iterate over all tracks
for track in tracks:
    # get the points
    points = track.points()
    # calculate the distance to the first point
    distance = np.linalg.norm(points[:, :] - points[0, :], axis=1)
    # plot the displacement
    plt.plot(distance, "-o")

# show the plot
plt.xlabel("# frame")
plt.ylabel("displacement (pixel)")
plt.show()
