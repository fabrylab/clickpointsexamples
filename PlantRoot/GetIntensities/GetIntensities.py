from __future__ import division, print_function
import re
import numpy as np
from matplotlib import pyplot as plt
import clickpoints

class Addon(clickpoints.Addon):
    def __init__(self, *args, **kwargs):
        clickpoints.Addon.__init__(self, *args, **kwargs)
        plt.figure(0)

    def run(self, start_frame=0):
        # get images and mask_types
        images = self.db.getImages()
        mask_types = self.db.getMaskTypes()

        # regular expression to get time from filename
        regex = re.compile(r".*(?P<experiment>\d*)-(?P<time>\d*)min")

        # initialize arrays for times and intensities
        times = []
        intensities = []

        # iterate over all images
        for image in images:
            print("Image", image.filename)
            # get time from filename
            time = float(regex.match(image.filename).groupdict()["time"])
            times.append(time)

            # get mask and green channel of image
            mask = image.mask.data
            green_channel = image.data[:, :, 1]

            # sum the pixel intensities for every channel
            intensities.append([np.mean(green_channel[mask == mask_type.index]) for mask_type in mask_types])

        # convert lists to numpy arrays
        intensities = np.array(intensities).T
        times = np.array(times)

        # iterate over cells
        for mask_type, cell_int in zip(mask_types, intensities):
            plt.plot(times, cell_int, "-s", label=mask_type.name)

        # add legend and labels
        plt.legend()
        plt.xlabel("time (min)")
        plt.ylabel("mean intensity")
        # display the plot
        plt.show()
