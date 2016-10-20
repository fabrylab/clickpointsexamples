import matplotlib.pyplot as plt
import numpy as np
import clickpoints
import io

# Simulation parameters
N = 10
size = 100
size = 100
frame_count = 100

# create new database
db = clickpoints.DataFile("sim.cdb", "w")

# Create a new marker type
type_point = db.setMarkerType("point", "#FF0000", mode=db.TYPE_Track)

# Create track instances
tracks = [db.setTrack(type_point) for i in range(N)]

# Create initial positions
points = np.random.rand(N, 2)*size

# iterate
for i in range(frame_count):
    print(i)
    # Create a new frame
    image = db.setImage("frame_%03d" % i, width=size, height=size)

    # Move the positions
    points += np.random.rand(N, 2)-0.5

    # Save the new positions
    db.setMarkers(image=image, x=points[:, 0], y=points[:, 1], track=tracks)

# plot the results
for track in tracks:
    plt.plot(track.points[:, 0], track.points[:, 1], '-')
plt.xlim(0, size)
plt.ylim(size, 0)
plt.show()
