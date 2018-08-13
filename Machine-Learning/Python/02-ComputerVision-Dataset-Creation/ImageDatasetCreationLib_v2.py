# Helpful link:
# https://auth0.com/blog/image-processing-in-python-with-pillow/

# Run this to show plots, figures, etc. within ipython terminal
#%pylab

# Imports
import os, tarfile, glob, shutil, h5py
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
import PIL

# Define settings for use below
settings = {
    "archiveDirectory": "sourceData", 
    "petArchiveFile": "petImages.tar.gz",
    "objectArchiveFile": "101_ObjectCategories.tar.gz",
    "petExtractDirName": "images",
    "objectExtractDirName": "101_ObjectCategories",
    "petOutputDirectory": "catImages",
    "objectOutputDirectory": "objectImages",
    "petProcessedDirectory": "catImagesProcessed",
    "objectProcessedDirectory": "objectImagesProcessed",
    "resizeDim" : 64
}

# Clean up any previous files and directories
def clean(settings):
    print("Cleaning...\n")

    # Clean up the raw files extracted from the source archive files
    archiveDirectory = os.path.join(os.getcwd(), settings["archiveDirectory"])
    path = os.path.join(os.getcwd(), archiveDirectory, settings["petExtractDirName"])
    print("Removing " + str(path))
    shutil.rmtree(path, True)
    path = os.path.join(os.getcwd(), archiveDirectory, settings["objectExtractDirName"])
    print("Removing " + str(path))
    shutil.rmtree(path, True)

    # Clean up the files that were sorted and renamed out of the source archive extract area
    path = os.path.join(os.getcwd(), settings["petOutputDirectory"])
    print("Removing " + str(path))
    shutil.rmtree(path, True)
    path = os.path.join(os.getcwd(), settings["objectOutputDirectory"])
    print("Removing " + str(path))
    shutil.rmtree(path, True)

    # Clean up any processed files (i.e. resized, aspect ratio altered, etc.)
    path = os.path.join(os.getcwd(), settings["petProcessedDirectory"])
    print("Removing " + str(path))
    shutil.rmtree(path, True)
    path = os.path.join(os.getcwd(), settings["objectProcessedDirectory"])
    print("Removing " + str(path))
    shutil.rmtree(path, True)

    print("\nDone...")
    return

# Extract the contents of an archive
def unpack(archiveDirectory, archiveFile, outputDirectory, extractDirName):
    # Get path to archive file to unpack
    archive = os.path.join(os.getcwd(), archiveDirectory, archiveFile)

    # Create a new directory for future use when we sort and rename the files pulled from the archive
    output = os.path.join(os.getcwd(), outputDirectory)
    os.makedirs(os.path.join(os.getcwd(), output), exist_ok=True)

    # Extract the images from the archive
    with tarfile.open(archive, 'r:gz')as tar:
        tar.extractall(archiveDirectory)
        tar.close()

    # Store the path to the extracted directory that is created when the archive is unpacked
    extractedPath = os.path.join(os.getcwd(), archiveDirectory, extractDirName)

    return output, extractedPath

# Extract the image archives and move the source image files into a staging area
def unpackImageArchives(settings):
    # Init counters
    catCount = 0
    objectCount = 0
    
    # Unpack the cat images
    print("Unpacking and sorting the pet images...")

    # Define directory names
    archiveDirectory = settings["archiveDirectory"]
    archiveFile = settings["petArchiveFile"]
    outputDirectory = settings["petOutputDirectory"]
    extractDirName = settings["petExtractDirName"]

    # Unpack the images and record the extract and staging folder locations
    output, extractedPath = unpack(archiveDirectory, archiveFile, outputDirectory, extractDirName)
    # Define what kind of images we want to iterate over
    imageFilter = os.path.join(extractedPath, '**', '*.jpg')

    # Move the image files from sub folders into a main area for later processing
    for filename in glob.iglob(imageFilter, recursive=True):
        # Look at first letter in file name; upper == cat && lower == dog
        if Path(filename).name[0].isupper():
            catCount += 1
            toPath = os.path.join(output, Path(filename).name)
            os.rename(filename, toPath)

    # Remove the raw, source files that were unpacked from the archive
    shutil.rmtree(extractedPath)
    
    # Unpack the object images
    print("Unpacking and sorting the object images...")

    # Define directory names
    archiveFile = settings["objectArchiveFile"]
    outputDirectory = settings["objectOutputDirectory"]
    extractDirName = settings["objectExtractDirName"]

    # Unpack the images and record the extract and staging folder locations
    output, extractedPath = unpack(archiveDirectory, archiveFile, outputDirectory, extractDirName)
    # Define what kind of images we want to iterate over
    imageFilter = os.path.join(extractedPath, '**', '*.jpg')
    # Define list of object images to skip
    skip = ['BACKGROUND_Google', 'cougar_body', 'cougar_face', 'dalmatian', 'garfield', 'Leopards', 'snoopy', 'wild_cat']

    # Move the image files from sub folders into a main area for later processing
    for filename in glob.iglob(imageFilter, recursive=True):
        # Skip any image categories we don't want in our final data set
        if Path(filename).parts[-2] in skip:
            continue
        objectCount += 1
        toPath = os.path.join(output, Path(filename).parts[-2] + "-" + Path(filename).name)
        os.rename(filename, toPath)

    # Remove the raw, source files that were unpacked from the archive
    shutil.rmtree(extractedPath)
    
    # We're done; provide some simple metrics
    print("\nDone!\n")
    print("Total files sorted:" + str(catCount + objectCount))
    print("Total cats:" + str(catCount))             
    print("Total objects:" + str(objectCount))
    print("\n")
    
    return catCount, objectCount

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

# Return a random selection of images from a given directory
def shuffle(inputDir, numberToReturn):
    images = glob.glob(inputDir + "/*.jpg")
    return np.random.choice(images, size=numberToReturn, replace=False, p=None)

# Assumes we are creating a sample for a binary classifier
# So we want to return a sample of Yes|No images (i.e. Yes, a cat; No, not a cat)
def createSample(yesDir, noDir, numYes, numNo, percentTest, randomState = 10):
    # Pull a random sample of each type of image (Yes|No)
    yesImages = shuffle(yesDir, numYes)
    noImages = shuffle(noDir, numNo)
    
    # Create the label array
    labels = np.zeros((numYes+numNo), dtype=int)
    labels[range(0, numYes)] = 1
    
    # Concat the image samples; Yes first then No
    images = np.concatenate((yesImages, noImages))
    
    # Now shuffle everything up, so we have a random sample of Yes and No images
    permutation = list(np.random.permutation(len(labels)))
    labels = labels[permutation]
    images = images[permutation]
    
    # Slice the labels and images into test and train sets
    trainFiles, testFiles, trainLabels, testLabels = train_test_split(
        images, labels, test_size = percentTest, random_state = randomState)
    
    trainLabels = [trainLabels]
    testLabels = [testLabels]
        
    return trainFiles, testFiles, trainLabels, testLabels

# Read image(s) into an Numpy array and return the collection of Numpy image arrays
def makeImageData(files, dim = 128, debug = False):
    dataSet = []

    for f in files:
        if debug: print(f)
        img = PIL.Image.open(f).convert('RGB')
        img = img.resize((dim, dim), PIL.Image.ANTIALIAS)
        img = np.asarray(img)
        dataSet.append(img)

    if debug:
        print("len(dataSet):", len(dataSet))
        print("dataSet[0].shape", dataSet[0].shape)
        plt.imshow(dataSet[0])
    
    return dataSet

# Write the train and test labels and images to a HDF5 container
def writeArch(outputFile, trainData, trainLabels, testData, testLabels):
    print("Creating HDF5 archive file...\n")
    
    with h5py.File(outputFile, "w") as archive:
        archive.create_dataset("trainData", data=trainData)
        archive.create_dataset("trainLabels", data=trainLabels)
        archive.create_dataset("testData", data=testData)
        archive.create_dataset("testLabels", data=testLabels)
        archive.close()
    
    # Check the size on disk
    print("Archive created.\n")
    sizeOnDiskKB = round(os.path.getsize(outputFile) / 1024, 1)
    sizeOnDiskMB = round(sizeOnDiskKB / 1024, 1)
    print(str(outputFile) + " written to disk.  File size: " + str(sizeOnDiskKB) + "(kb) / " + str(sizeOnDiskMB) + "(mb)\n\n")
    
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