# Load libraries
import os

import numpy as np
from numpy import arange

from matplotlib import pyplot

from pandas import read_csv
from pandas import set_option
from pandas.plotting import scatter_matrix
from pandas import DataFrame

from sklearn.preprocessing import StandardScaler

from sklearn.decomposition import PCA

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet

from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import RFE

from sklearn.metrics import mean_squared_error



dataFile = os.path.join(".", "datasets", "housing.csv")
data = read_csv(dataFile, header = 0, delim_whitespace = True)



# Seperate X and Y values
x = data.values[:, 0:len(data.columns) - 1]
y = data.values[:, len(data.columns) - 1]

print("--------")
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




# Init vars
folds = 10
seed = 10
models = []
results = {}

# Use MSE since this is a regression problem
score = 'neg_mean_squared_error'

# Instantiate model objects
models.append(('LR', LinearRegression()))
models.append(('LASSO', Lasso()))
models.append(('EN', ElasticNet()))
models.append(('KNN', KNeighborsRegressor()))
models.append(('CART', DecisionTreeRegressor()))
models.append(('SVR', SVR()))

# Create a Pandas DF to hold all our spiffy results
df = DataFrame(columns = ['Model', 'MSE', 'StdDev'])

# Run the models
for modelName, model in models:
    # Implement K-fold cross validation where K = 10
    kFold = KFold(n_splits = folds, random_state = seed)
    results[modelName] = cross_val_score(model, xTrain, yTrain, cv = kFold, scoring = score)
    df.loc[len(df)] = list([modelName, results[modelName].mean(), results[modelName].std()])

# Print results sorted by Mean desc, StdDev asc, Model asc
print("--------")
print(df.sort_values(by = ['MSE', 'StdDev', 'Model'], ascending = [False, True, True]))




# Init vars and params
scaledModels = []
scaledResults = {}
scaledFolds = 10
scaledSeed = 10

# Use MSE since this is a regression problem
score = 'neg_mean_squared_error'

# Create a Pandas DF to hold all our spiffy results
scaledDF = DataFrame(columns = ['Model', 'MSE', 'StdDev'])

# Setup the pipelines
pipes = []

# Create the scaled model objects
for modelName, model in models:
    pipes.append(('scaled' + modelName, Pipeline([('Scaler', StandardScaler()),(modelName, model)])))

# Run the models
for modelName, model in pipes:
    # Implement K-fold cross validation where K = 10
    kFold = KFold(n_splits = scaledFolds, random_state = scaledSeed)
    scaledResults[modelName] = cross_val_score(model, xTrain, yTrain, cv=kFold, scoring = score)
    scaledDF.loc[len(scaledDF)] = list([modelName, scaledResults[modelName].mean(), scaledResults[modelName].std()])

# Print results sorted by Mean desc, StdDev asc, Model asc
print("--------")
print(scaledDF.sort_values(by = ['MSE', 'StdDev', 'Model'], ascending = [False, True, True]))




# Init vars and params
featureResults = {}
featureFolds = 10
featureSeed = 10

# Use MSE since this is a regression problem
score = 'neg_mean_squared_error'

# Create a Pandas DF to hold all our spiffy results
featureDF = DataFrame(columns = ['Model', 'MSE', 'Best Params'])

# Pipeline params
params = {
    'FeatureUnion__SelectFeatures__k': list(range(1,len(data.columns)))
}

# Create feature union
features = []
features.append(('Scaler', StandardScaler()))
features.append(('SelectFeatures', SelectKBest(f_regression)))
featureUnion = FeatureUnion(features)


# Setup the pipelines
pipes = []
for modelName, model in models:
    featureResults[modelName] = GridSearchCV(
        Pipeline(
            steps = [
                ('FeatureUnion', featureUnion),
                (modelName, model)
            ]),
        param_grid = params,
        scoring = score,
        cv = KFold(n_splits = featureFolds, random_state = featureSeed)      
    ).fit(xTrain, yTrain)

    featureDF.loc[len(featureDF)] = list([
        modelName, 
        featureResults[modelName].best_score_,
        featureResults[modelName].best_params_,
    ])
    
# Print results sorted by Mean desc, StdDev asc, Model asc
print("--------")
print(featureDF.sort_values(by = ['MSE', 'Model'], ascending = [False, True]))




# Create a Pandas DF to hold all our spiffy results
featureDF = DataFrame(columns = ['Model', 'MSE', 'Best Params'])

# Pipeline params
params = {
    'FeatureUnion__SelectFeatures__k': list(range(1,len(data.columns))),
    'KNN__n_neighbors' : list(range(1,25,2))
}

# Search for the best combination of parameters
knnResults = GridSearchCV(
    Pipeline(
        steps = [
            ('FeatureUnion', featureUnion),
            ('KNN', KNeighborsRegressor())
        ]),
    param_grid = params,
    scoring = score,
    cv = KFold(n_splits = featureFolds, random_state = featureSeed)      
).fit(xTrain, yTrain)

featureDF.loc[len(featureDF)] = list([
    'KNN', 
    knnResults.best_score_,
    knnResults.best_params_,
])

set_option('display.max_colwidth', -1)
print("--------")
print(featureDF)