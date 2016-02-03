from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt

from clickpoints.MarkerLoad import *

# open DB File
db = DataFile("clickpoints.db")

tracks = db.GetTracks()
for track in tracks:
    points = track.points()
    plt.plot(np.linalg.norm(points[:, :] - points[0, :], axis=1), "-o")
plt.show()
