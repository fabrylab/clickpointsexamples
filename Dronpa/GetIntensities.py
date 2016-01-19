from __future__ import division, print_function
import re
import imageio
import numpy as np
from matplotlib import pyplot as plt

from clickpoints.MarkerLoad import GetImages, GetMasks

def stderr(values):
    return np.std(values)/np.sqrt(len(values))

regex = re.compile(r".*(?P<experiment>\d*)-(?P<time>\d*)min")
images = GetImages()
cells = None
intensities = []
errorbars = []
times = []
for image_entry in images:
    mask_entry = GetMasks(image_entry.id, 0)

    print("Image", image_entry.filename)
    time = float(regex.match(image_entry.filename).groupdict()["time"])
    times.append(time)

    image = imageio.imread(image_entry.filename)[:, :, 1]
    mask = imageio.imread(mask_entry.filename)[:, :, 0]

    if cells is None:
        cells = np.array(np.unique(mask))
        cells = cells[1:]

    intensities.append([np.mean(image[mask == cell]) for cell in cells])
    errorbars.append([stderr(image[mask == cell]) for cell in cells])

intensities = np.array(intensities).T
errorbars = np.array(errorbars).T
for label, cell_int, error in zip(cells, intensities, errorbars):
    plt.errorbar(times, cell_int, error, label=label)
plt.legend()
plt.xlabel("time (min)")
plt.ylabel("mean intensity")
plt.show()
