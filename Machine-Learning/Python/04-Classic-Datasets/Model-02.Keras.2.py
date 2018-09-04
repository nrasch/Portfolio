%matplotlib inline
%load_ext autoreload
%autoreload 2

import warnings
warnings.filterwarnings('ignore')

#--------

# Load libraries
import os
import numpy as np
from numpy import arange
from math import sqrt
from matplotlib import pyplot
from pandas import read_csv
from pandas import set_option
from pandas.plotting import scatter_matrix
from pandas import DataFrame
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from keras.wrappers.scikit_learn import KerasRegressor
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.optimizers import SGD
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import RFE
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.metrics import mean_squared_error

#--------

dataFile = os.path.join(".", "datasets", "housing.csv")
data = read_csv(dataFile, header = 0, delim_whitespace = True)

#--------

def makeRange(start, stop, step = 1, multi = 1, dec = 1):
    vals = []
    for i in range(start, stop, step):
        vals.append(np.round(multi * i, decimals = dec))
        
    return vals

#--------

print("--------")
# Seperate X and Y values
x = data.values[:, 0:len(data.columns) - 1]
y = data.values[:, len(data.columns) - 1]

print("x.shape = ", x.shape)
print("y.shape = ", y.shape)

# Split out validation set -- 80/20 split
seed = 10
valSize = 0.2

xTrain, xVal, yTrain, yVal = train_test_split(x, y, test_size = valSize, random_state = seed)

print("--------")
print("xTrain.shape = ", xTrain.shape)
print("yTrain.shape = ", yTrain.shape)
print("xVal.shape = ", xVal.shape)
print("yVal.shape = ", yVal.shape)

#--------

def buildModel(optimizer = 'Adam', lr = 0.001, decay = 0.0, epsilon = None):
    opt = None
    
    model = Sequential()
    
    # kernel_initializer='normal' -> Initializer capable of adapting its scale to the shape of weights
    # bias_initializer -> 'zeros' (default per the docs)
    
    #model.add(Dense(20, input_dim = xTrain.shape[1], kernel_initializer='normal', activation = 'relu'))
    #model.add(Dense(20, input_dim = 18, kernel_initializer='normal', activation = 'relu'))
    model.add(Dense(20, kernel_initializer='normal', activation = 'relu'))
    model.add(Dense(10, kernel_initializer='normal', activation = 'relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    
    if optimizer.lower() == 'adam':
        opt = Adam(lr = lr, decay = decay, epsilon = epsilon)
    else:
        # Please don't ever use eval where you're recieving input from non-trusted sources!
        # A Jupyter notebook is OK; a public facing service is certainly not
        opt = eval(optimizer)()
    
    model.compile(loss = 'mean_squared_error', optimizer = opt)
    
    return model   

#--------

print("--------")
print("INITIAL PASS")

# Define vars and init
folds = 10
seed = 10

np.random.seed(seed)

model = KerasRegressor(build_fn = buildModel, epochs = 200, batch_size = 5, verbose = 0)
kFold = KFold(n_splits = folds, random_state = seed)
results = cross_val_score(model, xTrain, yTrain, cv = kFold)

print("MSE: %.2f (%.2f)" % (results.mean(), results.std()))

#--------

def tuneModel(modelName, modelObj, params, iterations = 20, returnModel = False, showSummary = True):
    # Init vars and params
    featureResults = {}
    featureFolds = 10
    featureSeed = 10
    
    np.random.seed(featureSeed)
    
    # Use MSE since this is a regression problem
    score = 'neg_mean_squared_error'

    # Create a Pandas DF to hold all our spiffy results
    featureDF = DataFrame(columns = ['Model', 'MSE', 'StdDev', 'Best Params'])

    # Create feature union (adding SelectKBest)
    features = []
    features.append(('Scaler', StandardScaler()))
    features.append(('SelectKBest', SelectKBest()))
    featureUnion = FeatureUnion(features)

    # Search for the best combination of parameters
    featureResults = RandomizedSearchCV(
        Pipeline(
            steps = [
                ('FeatureUnion', featureUnion),
                (modelName, modelObj)
        ]),
        param_distributions = params,
        n_iter = iterations,
        scoring = score,
        cv = KFold(n_splits = featureFolds, random_state = featureSeed),
        random_state = featureSeed
    ).fit(xTrain, yTrain)

    featureDF.loc[len(featureDF)] = list([
        modelName, 
        featureResults.best_score_,
        featureResults.best_params_,
        featureResults.cv_results_['std_test_score'][featureResults.best_index_]
    ])

    if showSummary:
        set_option('display.max_colwidth', -1)
        display(featureDF)
    
    if returnModel:
        return featureResults

#--------

print("--------")
print("FIRST EXECUTION")

modelName = "housingModel"
modelObj =  KerasRegressor(build_fn = buildModel, verbose = 0)
params = {
    'housingModel__optimizer' : ['Adam'],
    'housingModel__epochs' : makeRange(200, 600, 50),
    'housingModel__batch_size' : makeRange(4, 68, 4),
    'FeatureUnion__SelectKBest__k': makeRange(1, xTrain.shape[1]),
    'housingModel__lr' : makeRange(1, 9, 1, .001, 3),
    'housingModel__epsilon' : makeRange(2, 8, 1, .5, 1),
}

set1 = tuneModel(modelName, modelObj, params, 90, True, True)

#--------

print("--------")
set_option('precision', 3)
print(DataFrame(set1.cv_results_).sort_values(by=['mean_test_score', 'std_test_score'], ascending=False))
