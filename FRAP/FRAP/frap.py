# frap.py

# Copyright (c) 2015-2016, Richard Gerum, Sebastian Richter
#
# This file is part of ClickPoints.
#
# ClickPoints is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ClickPoints is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ClickPoints. If not, see <http://www.gnu.org/licenses/>

from __future__ import print_function, division
import clickpoints
import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt


class Addon(clickpoints.Addon):
    def __init__(self, *args, **kwargs):
        clickpoints.Addon.__init__(self, *args, **kwargs)

        # Check if the marker types are present
        if not self.db.getMarkerType("FRAP_bleach"):
            self.db.addMarkerType("FRAP_bleach", [0, 255, 0], self.db.TYPE_Rect)
            self.cp.reloadTypes()
        if not self.db.getMarkerType("FRAP_background"):
            self.db.addMarkerType("FRAP_background", [0, 128, 0], self.db.TYPE_Rect)
            self.cp.reloadTypes()

        plt.figure(0)

    def run(self, start_frame=0):
        # try to load marker
        rects_bleach = self.db.getRectangles(type="FRAP_bleach")
        rects_background = self.db.getRectangles(type="FRAP_background")

        # check if we have at least one bleach region
        if len(rects_bleach) < 1:
            print("ERROR: no rectangle selected.\nPlease mark a rectangle with type 'FRAP_bleach'.")
            return

        # get all the images
        images = self.db.getImages()

        # define empty lists
        bleach = []  # bleach should store for each bleach region the mean intensity over time
        background = []  # background should store the mean over all background regions over time
        # start iteration
        for image in images:
            # go through all bleach regions and extract the mean intensity
            bleach_values = []
            for bleach_rect in rects_bleach:
                bleach_values.append(np.mean(image.data[bleach_rect.slice_y(), bleach_rect.slice_x()]))
            bleach.append(bleach_values)
            # go through all the background regions and sum up the mean intensity
            background_value = 0
            for background_rect in rects_background:
                background_value += np.mean(image.data[background_rect.slice_y(), background_rect.slice_x()])
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
