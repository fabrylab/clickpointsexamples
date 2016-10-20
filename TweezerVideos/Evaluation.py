from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt

# connect to ClickPoints database
# database filename is supplied as command line argument when started from ClickPoints
import clickpoints
start_frame, database, port = clickpoints.GetCommandLineArgs()
db = clickpoints.DataFile(database)

# get all tracks
tracks = db.getTracks()

# iterate over all tracks
for track in tracks:
    # get the points
    points = track.points_corrected
    # calculate the distance to the first point
    distance = np.linalg.norm(points[:, :] - points[0, :], axis=1)
    # plot the displacement
    plt.plot(track.frames, distance, "-o")

# show the plot
plt.xlabel("# frame")
plt.ylabel("displacement (pixel)")
plt.show()
