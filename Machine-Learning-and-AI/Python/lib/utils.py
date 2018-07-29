# Imports
import os, h5py
from matplotlib import pyplot as plt
import numpy as np


# Define settings for use below
settings = {
    "resizeDim" : 128
}

# Helper function to display grid of images - Borrowed from Stackoverflow
def grid_display(list_of_images, list_of_titles=[], no_of_columns=2, figsize=(10,10)):
    fig = plt.figure(figsize=figsize)
    column = 0
    for i in range(len(list_of_images)):
        column += 1
        #  check for end of column and create a new figure
        if column == no_of_columns+1:
            fig = plt.figure(figsize=figsize)
            column = 1
        fig.add_subplot(1, no_of_columns, column)
        plt.imshow(list_of_images[i])
        plt.axis('off')
        if len(list_of_titles) >= len(list_of_images):
            plt.title(list_of_titles[i])
    return

# Access a given HDF5 image dataset archive file and inspect the contents
def validateArchive(archiveFile, imagesToShow = 20):
    # Open and read the HDF5 container
    with h5py.File(archiveFile, "r") as archive:
        print("*** KEYS")
        print("HDF5 container keys: " + str(list(archive.keys())) + "\n")
       
        # Pull and examine the labels from the HDF5 container
        print("*** LABELS")

        trainLabels = np.array(archive["trainLabels"][:])
        testLabels = np.array(archive["testLabels"][:])
        
        print("Total number of training labels:", trainLabels.shape[1])
        print("Number of cat labels:", np.count_nonzero(trainLabels > 0))
        print("Number of object labels:", np.count_nonzero(trainLabels < 1))
        print("First 10 training labels:", trainLabels[0][0:9])
        print("\n")
        
        print("Total number of testing labels:", testLabels.shape[1])
        print("Number of cat labels:", np.count_nonzero(testLabels > 0))
        print("Number of object labels:", np.count_nonzero(testLabels < 1))
        print("First 10 testing labels:", testLabels[0][0:9])
        print("\n")
        
        
        # Pull and examine the training data from the HDF5 container
        print("*** IMAGE DATA")
        
        trainData = np.array(archive["trainData"][:])
        print("Image data shape in archive:", trainData.shape)
        print("\n")
        
        # Pull first image and examine it
        item = trainData[0]
        print("First HDF5 container dataSet item shape:", item.shape)
        flatItem = item.reshape(item.shape[0], -1).T
        print("Image data shape after flattening:", flatItem.shape)
        print("First 10 dataSet item matrix values:", flatItem[100,100:110])
        print("\n")

        # View the image
        print("Recreating and showing first", imagesToShow, "images from flattened matrix values:\n")
        images = []
        for i in range(0, imagesToShow):
            images.append(trainData[i].reshape((settings["resizeDim"], settings["resizeDim"], 3)))
        grid_display(images, [], 5, (10,10))

        # Close the HDF5 container
        archive.close()

    return