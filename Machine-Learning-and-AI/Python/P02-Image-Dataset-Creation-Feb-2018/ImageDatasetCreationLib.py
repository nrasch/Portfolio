# Run this to show plots, figures, etc. within ipython terminal
#%pylab

# Imports
import os, tarfile, glob, shutil, cv2, h5py
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

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
    skip = ['BACKGROUND_Google', 'cougar_body', 'cougar_face', 'dalmatian', 'garfield', 'Leopards', 'snoopy']

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

# Display some number of images from a given directory
def displayImages(numberToShow, imagePath):
    # Container for the images we want to show in a grid
    images = []
    # Define what kind of images we want to iterate over
    imageFilter = os.path.join(imagePath, '**', '*.jpg')

    # Display the N number of images found in the given image director
    for filename in glob.iglob(imageFilter, recursive=True):
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        images.append(image)
        if len(images) == numberToShow:
            break
            
    # Show the images we've collected
    grid_display(images, [], 5, (10,10))

    return

# Alter the aspect ratio of some number of images into a square shape
def squareImages(inputDir, outputDir, numberToProcess):
    print("Starting to square images...")
    
    # Container to store the names of the image files processed
    images = []
    skipped = []

    # Create the processed image output directory
    os.makedirs(os.path.join(os.getcwd(), outputDir), exist_ok=True)

    # For each image:
        # Determine which side of the image is bigger than the other
        # Calculate the size difference between the sides
        # Reduce the longer side to the same dimension as the shorter side
        # while keeping the image centered

    # Define what kind of images we want to iterate over
    imageFilter = os.path.join(inputDir, '**', '*.jpg')

    # Square up each image found:
    for filename in glob.iglob(imageFilter, recursive=True):
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        
        # There are six cat and one object image that cause errors, so adding this check...
        if image is None:
            skipped.append(filename)
            continue
            
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        images.append(filename)
        
        if image.shape[0] > image.shape[1]:
            dimDiff = round((image.shape[0]-image.shape[1])/2, 0)
            cropRange =  range(int(dimDiff), int(image.shape[0]-dimDiff))
            image = image[cropRange, 1:image.shape[1]]
        elif image.shape[0] < image.shape[1]:
            dimDiff = round((image.shape[1]-image.shape[0])/2, 0)
            cropRange =  range(int(dimDiff), int(image.shape[1]-dimDiff))
            image = image[1:image.shape[0], cropRange]    

        # Save the modified image to disk
        cv2.imwrite(os.path.join(outputDir, Path(filename).name), image)
        
        if len(images) == numberToProcess:
            break

    print("Finished squaring images!")
    return images, skipped

# Resize some number of images into a specified size
def resizeImages(inputDir, outputDir, newImageSize, numberToProcess):
    print("Starting to resize images...")
    
    # Container to store the names of the image files processed
    images = []
    # Store the number of pixels for a processed image
    features = False

    # Create the processed image output directory
    os.makedirs(os.path.join(os.getcwd(), outputDir), exist_ok=True)

    # Define what kind of images we want to iterate over
    imageFilter = os.path.join(inputDir, '**', '*.jpg')

    # Resize each image found:
    for filename in glob.iglob(imageFilter, recursive=True):
        images.append(filename)
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (newImageSize, newImageSize))

        # Save the modified image to disk
        cv2.imwrite(os.path.join(outputDir, Path(filename).name), image)
        #plt.imshow(image)
        if len(images) == numberToProcess:
            break

        # Record the number of pixels in the modified image
        if not features:
            features = np.prod(image.shape)

    print("Finished resizing images!")
    return features, images

# Return a random selection of images from a given directory
def shuffle(inputDir, numberToReturn):
    imageFilter = os.path.join(inputDir, '**', '*.jpg')
    images = glob.glob(imageFilter, recursive=True)
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
    return train_test_split(images, labels, test_size = percentTest, random_state = randomState)

# Reduce images from a three channel matrix to a (1,x) array of standardized values
def flattenImages(features, images):
    # We want one column entry for each image, and a row entry for each pixel color value (i.e. features)
    dataSet = np.zeros((features, len(images)))

    # Next we flatten and standardize each image and store it in the dataSet container
    for i, image in enumerate(images):
        image = cv2.imread(os.path.join(os.getcwd(), image), cv2.IMREAD_COLOR)
        dataSet[:, i] = image.flatten() / 255

    return dataSet


# Write the train and test labels and images to a HDF5 container
def createArchive(outputFile, trainLabels, testLabels, trainImages, testImages, features = 12288):
    print("Creating HDF5 archive file...\n")

    # Create the HDF5 container and add the sample data we've created
    with h5py.File(outputFile, "w") as archive:
        archive.create_dataset("trainLabels", data=trainLabels)
        archive.create_dataset("testLabels", data=testLabels)
        archive.create_dataset("trainImages", data=flattenImages(features, trainImages))
        archive.create_dataset("testImages", data=flattenImages(features, testImages))
        archive.close()

    # Check the size on disk
    print("Archive created.\n")
    sizeOnDiskKB = round(os.path.getsize(outputFile) / 1024, 1)
    sizeOnDiskMB = round(sizeOnDiskKB / 1024, 1)
    print(str(outputFile) + " written to disk.  File size: " + str(sizeOnDiskKB) + "(kb) / " + str(sizeOnDiskMB) + "(mb)")

    return archive

# Quick and dirty test to ensure the HDF5 archive file was created correctly
def validateArchive(archiveFile):
    # Open and read the HDF5 container
    with h5py.File(archiveFile, "r") as archive:
        print("*** KEYS")
        print("HDF5 container keys: " + str(list(archive.keys())) + "\n")
       
        print("*** LABELS")

        # Pull and examine the training labels from the HDF5 container
        cData = np.array(archive['testLabels'])
        print("Total number of testing labels:", len(list(cData)))
        print("Number of cat labels:", np.count_nonzero(cData > 0))
        print("Number of object labels:", np.count_nonzero(cData < 1))
        print("First 10 testing labels:", list(cData)[1:10])
        print("\n")
        
        # Pull and examine the training labels from the HDF5 container
        cData = np.array(archive['trainLabels'])
        print("Total number of training labels:", len(list(cData)))
        print("Number of cat labels:", np.count_nonzero(cData > 0))
        print("Number of object labels:", np.count_nonzero(cData < 1))
        print("First 10 training labels:", list(cData)[1:10])
        print("\n")
        
        print("*** IMAGE DATA")

        # Pull and examine the training data from the HDF5 container
        cData = archive['trainImages']
        # Pull first image and examine it
        item = cData[:, 0]
        print("First HDF5 container dataSet item shape:", item.shape)
        print("First 10 dataSet item matrix values:", item[1:10])
        print("\n")

        # View the image
        print("Recreating image from flattened matrix values:\n")
        image = item.reshape((64, 64, 3))*255
        cv2.imwrite('archiveTest.jpg', image)
        image = cv2.imread('archiveTest.jpg', cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image)

        # Close the HDF5 container
        archive.close()

    return