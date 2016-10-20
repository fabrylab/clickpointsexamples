import matplotlib.pyplot as plt
import clickpoints

# open database
db = clickpoints.DataFile("count.cdb")

# iterate over images
for index, image in enumerate(db.getImages()):
    # get count of adults in current image
    marker = db.getMarkers(image=image, type="adult")
    plt.bar(index, marker.count(), color='b', width=0.3)

    # get count of juveniles in current image
    marker = db.getMarkers(image=image, type="juvenile")
    plt.bar(index+0.3, marker.count(), color='r', width=0.3)

# display the plot
plt.show()
