##################
##### IMPORTS#####
##################

import os, h5py
from matplotlib import pyplot as plt
import numpy as np
import random 
from os import path
import pandas as pd
from IPython.display import display, HTML
from matplotlib import pyplot as plt
import inspect
import time
import copy
import h5py
import math

random.seed(10)
np.random.seed(10)



####################################
##### LOAD THE TEST/TRAIN DATA #####
####################################

# Define settings for use below
settings = {
    "resizeDim" : 64
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

def loadData():
    # Examine the data used for training the model
    imageData = path.join("datasets", "imageData500_64pixels.hdf5")
    
    # Load, shape, and normalize the data used for training the model
    with h5py.File(imageData, "r") as archive:   
        trainingData = np.squeeze(archive["trainData"][:])
        testData = np.squeeze(archive["testData"][:])
        trainingLabels = np.array(archive["trainLabels"][:])
        testLabels = np.array(archive["testLabels"][:])
        archive.close()

    print("Archive trainingData.shape:    ", trainingData.shape)
    print("Archive trainingLabels.shape:  ", trainingLabels.shape)
    print("Archive testData.shape:        ", testData.shape)
    print("Archive testLabels.shape:      ", testLabels.shape)
    print("\n")

    # Reshape the training and test data and label matrices
    trainingData = trainingData.reshape(trainingData.shape[0], -1).T
    testData = testData.reshape(testData.shape[0], -1).T

    print ("Flattened, normalized trainingData shape:  " + str(trainingData.shape))
    print ("Flattened, normalized testData shape:      " + str(testData.shape))

    # Normalization
    trainingData = trainingData/255.
    testData = testData/255.
    
    validateArchive(imageData)
    
    return trainingData, trainingLabels, testData, testLabels
    
    
    
###################################    
##### MODEL UTILITY FUNCTIONS #####
###################################

# Write a function to show multiple graphs in the same figure
def printCostGraphs(costs, keys, cols, fsize = (15,6)):
    # Figure out how many rows and columns we need
    counter = 0
    rows = np.ceil(len(costs) / cols)
    fig = plt.figure(figsize = fsize)
    
    # Add each of the cost graphs to the figure
    for key in keys:
        c = np.squeeze(costs[key])
        sub = fig.add_subplot(rows, cols, counter + 1)
        sub.set_title('Epoch ' + str(key))
        sub.plot(c)
        counter = counter + 1
    
    # Draw the figure on the page
    plt.plot()
    plt.tight_layout()
    plt.show()
    
# Randomize values for hyperparameters based on a given key:value dictionary
class HPicker:
    
    def pick(self, ranges):
        hParams = {}
        
        # For each parameter key:val
        for key, value in ranges.items():
            if isinstance(value, list):
                start, stop, step = value
                vals = []

                # Create a range of possible values
                while (start < stop):
                    start = round(start + step, len(str(step)))
                    vals.append(start)

                # Pick one of the possible values randomly    
                hParams[key] = random.choice(vals)
            else:
                hParams[key] = value
            
        return hParams  
    
# Create a pandas dataframe with labeled columns to record model training results
def getResultsDF(hRanges):
    columns = list(hRanges.keys())
    df = pd.DataFrame(columns = columns)
    
    return(df)

# Do all the heavy lifting required when running N number of models with various hyperparameter configurations
def runModels(data, hRanges, epochs, layerSizes, silent = False):
    
    # Var inits
    picker = HPicker()
    resultsDF = getResultsDF(hRanges)
    costs = {}
    params = {}
    epoch = 0
    trainingData, trainingLabels, testData, testLabels = data
    
    print("\n*** Starting model training")
    
    while (epoch < epochs):
        
        # Get the random hyperparam values
        hparams = picker.pick(hRanges)
        hparams["Epoch"] = epoch
        
        # Randomize the number of layers in the network and the number of cells in each layer
        dims = list()
        dims.append(random.randrange(layerSizes[0], layerSizes[1], 1))
        dims.append(layerSizes[2])
        dims.append(layerSizes[3])
        hparams["networkDimensions"] = defineDimensions(trainingData, trainingLabels, dims)

        # Print a summary of the model about to be trained and its params to the user
        if silent is not True:
            print("Training epoch", epoch, "with params:  LR", hparams["Learning_Rate"], 
                  ", iterations", hparams["Iterations"], ", NN dims", (hparams["networkDimensions"])["hiddenLayerSizes"], 
                  ", lambda", hparams["Lambda"], ", and init. multi.", hparams["Weight_Multi"])

        # Train the model its given hyperparams and record the results
        params[epoch], costs[epoch],  hparams["Descending_Graph"] = model(
            trainingData, trainingLabels, hparams["networkDimensions"], hparams["Iterations"], 
            hparams["Learning_Rate"], hparams["Lambda"], hparams["Weight_Multi"], False)
        
        # Make predictions based on the model
        trainingPreds = predict(trainingData, params[epoch], trainingLabels)
        testPreds = predict(testData, params[epoch], testLabels)

        # Record prediction results
        hparams["Train_Acc"] = trainingPreds["accuracy"]
        hparams["Test_Acc"] = testPreds["accuracy"]
        hparams["Final_Cost"] = costs[epoch][-1]
        hparams["networkDimensions"] = str((hparams["networkDimensions"])["hiddenLayerSizes"])

        # Add model results to the pandas dataframe
        resultsDF.loc[epoch] = list(hparams.values())
        epoch = epoch + 1
        
    print("*** Done!\n")
    
    # Sort the dataframe so it's easier to find the results we are interested in
    resultsDF = resultsDF.sort_values(by = ['Descending_Graph', 'Test_Acc'], ascending = False)
  
    return resultsDF, params, costs

# Save a set of model parameters to disk
def writeParamsToDisk(fileName, params):
    # Create the HDF5 container and write params
    with h5py.File(fileName, "w") as paramsFile:
        for key in params.keys():
            dset = paramsFile.create_dataset(key, data=params[key])
        paramsFile.close()
        
# Read a set of model parameters from disk
def readParamsFromDisk(fileName):
    params = {}
    
    with h5py.File(fileName, 'r') as file:
        for key in file.keys():
            params[key] = file[key][()]
        file.close()
    
    return params

def createMiniBatches(data, labels, batchSize, seed):  
    m = data.shape[1]
    miniBatches = []
    
    # Shuffle the data and labels
    np.random.seed(seed)
    permutation = list(np.random.permutation(m))
    
    shuffledData = data[:, permutation]
    shuffledLabels = labels[:, permutation].reshape((1,m))
    
    # Create the mini batches
    # First take all the groupings that fit into the "batchSize" bucket
    batches = math.floor(m / batchSize)
    for i in range(0, batches):
        batchData = shuffledData[:, i * batchSize : (i + 1) * batchSize]
        batchLabels = shuffledLabels[:, i * batchSize : (i + 1) * batchSize]
        miniBatch = (batchData, batchLabels)
        miniBatches.append(miniBatch)
        
    # Next take the final grouping of records that are left over
    if m % batchSize != 0:
        batchData = shuffledData[:, batches * batchSize : m]
        batchLabels = shuffledLabels[:, batches * batchSize : m]
        miniBatch = (batchData, batchLabels)
        miniBatches.append(miniBatch)
        
    return miniBatches


#############################################    
##### N-LAYER NEURAL NETWORK MODEL CODE #####
#############################################

# Define the dimensions of the model
def defineDimensions(data, labels, layerSizes):
    nnDims = {}
    
    nnDims["hiddenLayerSizes"] = []
        
    # layers tuple w/ 3 values:  number of hidden units, layer cell count min, layer cell count max
    for i in range(0, layerSizes[0]):
        layerSize = random.randint(layerSizes[1], layerSizes[2])
        nnDims["hiddenLayerSizes"].append(layerSize)
    
    nnDims["numberInputs"] = data.shape[0]
    nnDims["numberOutputs"] = labels.shape[0]
    
    return nnDims;

#  Initialize model params (i.e. W and b)
def initilizeParameters(dimensionDict):

    params = {}
    lastDimSize = dimensionDict["numberInputs"]
    
    for index, size in enumerate(dimensionDict['hiddenLayerSizes'], start=1):
        wName = "w" + str(index)
        bName = "b" + str(index)
        
        # Initialize utilizing "He Initialization"
        np.random.seed(10)  # Yes, this has to be done every time...  :(
        params[wName] = np.random.randn(size, lastDimSize) * np.sqrt(2/lastDimSize)
        params[bName] = np.zeros((size, 1))
        lastDimSize = size
   
    # add final output layer
    wName = "w" + str(len(dimensionDict['hiddenLayerSizes']) + 1)
    bName = "b" + str(len(dimensionDict['hiddenLayerSizes']) + 1)
        
    # Initialize utilizing "He Initialization"
    np.random.seed(10)  # Yes, this has to be done every time...  :(
    params[wName] = np.random.randn(dimensionDict["numberOutputs"], lastDimSize) * np.sqrt(2/lastDimSize)
    
    params[bName] = np.zeros((dimensionDict["numberOutputs"], 1))
      
    return params

# Define ReLu activation
def relu(x):
    return x * (x > 0)

# Define ReLu derivative
def dRelu(x):
    return 1. * (x > 0)

# Perform forward propogation
def forwardPropagation(data, params, dropProb):
    
    # Init vars
    numLayers = (len(params))//2 
    cache = {}
    cache['a0'] = a = data

    # Process each layer of the NN
    for i in range(1, numLayers + 1):

        # Made the code below easier to read
        aPrev = cache['a' + str(i-1)]
        w = params['w' + str(i)]
        b = params['b' + str(i)]
       
        # Perform linear calculations & sanity check
        z = np.dot(w, aPrev) + b
        assert(z.shape == (w.shape[0], aPrev.shape[1]))
        
        # Perform sigmoid or ReLu activation
        if (i == numLayers):
            # last layer; sigmoid activation
            cache['a' + str(i)] = 1 / (1 + np.exp(-(z)))
            assert(cache['a' + str(i)].shape == z.shape)
        else:
            # Hidden layer; ReLu activation
            cache['a' + str(i)] = relu(z)
            assert(cache['a' + str(i)].shape == z.shape)
            
            # Dropout regularization
            np.random.seed(10)  # Yes, this has to be done every time...  :(
            cache['dropMask' + str(i)] = np.random.rand(cache['a' + str(i)].shape[0], cache['a' + str(i)].shape[1])
            cache['dropMask' + str(i)] = cache['dropMask' + str(i)] < dropProb
            cache['a' + str(i)] = cache['a' + str(i)] * cache['dropMask' + str(i)]
            cache['a' + str(i)] = cache['a' + str(i)] / dropProb
        
    # Final sanity check
    assert(cache['a' + str((len(params))//2)].shape == (1, data.shape[1]))
        
    return cache

# Calculate the cost of the model (includes L2 regularization)
def calculateCost(labels, params, cache, lamb):
    # Define vars to make reading and writing the formulas easier below...
    regSums = 0
    m = labels.shape[1]  
    aL = cache['a' + str((len(params))//2)]
         
    # Perform cost and regularization calculations
    crossEntropyCost = (-1/m) * np.sum( (labels * np.log(aL)) + ((1-labels) * np.log(1-aL)) )
    
    layers = (len(params)//2) + 1
    for i in range(1, layers):
        regSums = regSums + np.sum(np.square(params['w' + str(i)]))
    
    l2RegularizationCost = (1/m) * (lamb/2) * regSums
    finalCost = crossEntropyCost + l2RegularizationCost
    
    return finalCost

# Perform linear back propogation
def linearBackProp(dz, aPrev, w, b, lamb): 
    m = aPrev.shape[1]    
    dw = (1 / m) * np.dot(dz, aPrev.T) + (lamb * w)/m
    db = (1 / m) * np.sum(dz, axis = 1, keepdims = True)
    
    # Sanity check
    assert (dw.shape == w.shape)
    assert (db.shape == b.shape)
  
    return dw, db

# Perform backward propogation
def backwardPropagation(labels, cache, params, lamb, dropProb):
    
    # Init variables
    grads = {}
    layers = (len(params)//2)
    
    # Make the code below easier to read
    aL = cache['a' + str(layers)]
    dw = "dw" + str(layers)
    db = "db" + str(layers)
    aPrev = 'a' + str(layers-1)
    w = 'w' + str(layers)
    b = 'b' + str(layers)
    m = aL.shape[1]
    

    # Initialize backprop:  Calc dz, dw, and db for layer L
    dz = aL - labels
    grads[dw], grads[db] = linearBackProp(dz, cache[aPrev], params[w], params[b], lamb)
       
    # Backprop for the hidden layers
    for i in reversed(range(1, layers)):
        
        # Make the code below easier to read
        dw = "dw" + str(i)
        db = "db" + str(i)
        a = 'a' + str(i)
        aPrev = 'a' + str(i-1)
        dzBefore = dz
        w = 'w' + str(i)
        wBefore = 'w' + str(i+1)
        b = 'b' + str(i)
        m = aL.shape[1]
        dropMask = 'dropMask' + str(i)
        
        # Apply backprop with dropout regularization and calc grads; breaking up the calc steps for readability
        # dz = np.dot(params[wBefore].T, dzBefore) * dRelu(cache[a])
        dz = np.dot(params[wBefore].T, dzBefore)
        dz = dz * cache[dropMask]
        dz = dz / dropProb
        dz = dz * dRelu(cache[a])
        grads[dw], grads[db] = linearBackProp(dz, cache[aPrev], params[w], params[b], lamb)
    
    return grads

# Update the model params based on the results of the backward propogation calculations
def updateParams(params, grads, learningRate):
    layers = (len(params)//2)
    
    for l in range(layers):
        params["w" + str(l + 1)] = params["w" + str(l + 1)] - learningRate * grads["dw" + str(l + 1)]
        params["b" + str(l + 1)] = params["b" + str(l + 1)] - learningRate * grads["db" + str(l + 1)]
   
    return params

# Define the actual neural network classification model
def model(data, labels, dims, numIterations, learningRate, lamb, batchSize, dropProb, printCost = False, showGraph = False):
    
    # Init vars
    params = initilizeParameters(dims)
    seed = 10
    
    #return params;
    
    costs = []
    descendingGraph = True
    
    # For each training iteration
    for i in range(0, numIterations + 1):
         
        # Create the mini batches
        seed = seed + 1   # assure we get a different batch composition each time through
        miniBatches = createMiniBatches(data, labels, batchSize, seed)
        
        for batch in miniBatches:
        
            # Get a set of data and lable records
            (batchData, batchLabels) = batch
            
            # Forward propagation
            cache = forwardPropagation(batchData, params, dropProb)

            # Cost function
            cost = calculateCost(batchLabels, params, cache, lamb)

            # Backward  propagation
            grads = backwardPropagation(batchLabels, cache, params, lamb, dropProb)

            # Gradient descent parameter update
            params = updateParams(params, grads, learningRate)
        
        # Print the cost every N number of iterations
        if printCost and i % 500 == 0:
            print ("Cost after iteration", str(i), "is", str(cost))
        
        # Record the cost every N number of iterations
        if i % 50 == 0:
            if (len(costs) != 0) and (cost > costs[-1]):
                descendingGraph = False
            costs.append(cost)
      
    # Print the model training cost graph
    if showGraph:
        _costs = np.squeeze(costs)
        plt.plot(_costs)
        plt.ylabel('Cost')
        plt.xlabel('Iterations (every 50)')
        plt.title("Learning rate =" + str(learningRate))
        plt.show()

    return params, costs, descendingGraph

# Utilize the model's trained params to make predictions
def predict(data, params, trueLabels):
    # Apply the training weights and the sigmoid activation to the inputs
    cache = forwardPropagation(data, params, 1)
    aL = cache['a' + str((len(params))//2)]
    
    # Classify anything with a probability of greater than 0.5 to a 1 (i.e. cat) classification
    predictions = (aL > 0.5)
    accuracy = 100 - np.mean(np.abs(predictions - trueLabels)) * 100
    
    preds = {"predictions" : predictions, "accuracy": accuracy}

    return preds
