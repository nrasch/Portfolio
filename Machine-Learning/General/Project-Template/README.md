# ML Project Template (work in progress...)

# Define project (i.e. goals, desired outcomes, etc.)

# Obtain data

Some good public data sets:

* https://archive.ics.uci.edu/ml/index.php

# Explore data

Non-visual (should probably put this into a table format...):
* View rows/columns 
```python
data.shape
```
* View first N records
```python
data.head(20)
```
* View data types:  `data.dtypes`
* View descriptive statistics:  `data.describe()`
* View classes:  `data.groupby('class').size()`
* correlation:  data.corr(method = "pearson")
* skew:  data.skew()


Visual:

* histogram:  
```python
data.hist(figsize = (8,8))
pyplot.show()
```

* density
```python
data.plot(kind = 'density', subplots = True, layout = (2,2), sharex = False, figsize = (8,8))
pyplot.show()
```

* box
```python
data.plot(kind="box", subplots = True, layout = (2,2), sharex = False, sharey = False, figsize = (8,8))
pyplot.show()
```

* scatter matrix
```python
scatter_matrix(data, figsize=(10, 10), s = 200)
pyplot.show()
```

* heat
```python
figure = pyplot.figure()
axis = figure.add_subplot(111)
graph = axis.matshow(corr, vmin = -1, vmax = 1)
figure.colorbar(graph)
ticks = np.arange(0, 4, 1)
axis.set_xticks(ticks)
axis.set_yticks(ticks)
axis.set_xticklabels(list(data)[0:4], rotation='45')
axis.set_yticklabels(list(data)[0:4])
pyplot.show()
``` 

# Prepare data

## Methods
* Rescale data
* Standardize data
* Normalize data
* Binarize data

### Links
* http://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing

## Pipelines

* http://queirozf.com/entries/scikit-learn-pipeline-examples



## Which models need which sort of data processing?
* https://www.dataschool.io/comparing-supervised-learning-algorithms/
* 


## Create train, validation, and test sets

Standard test_train_split
Downsampling
Stratified Sampling 

# Evaluate models

Estimator selection decision graphs:

* http://scikit-learn.org/stable/tutorial/machine_learning_map/index.html
* https://silvrback.s3.amazonaws.com/uploads/a43ca7b6-a235-46f8-a18e-ed95ad73caa1/ml_map_v4.png


Estimator documentation:
* http://scikit-learn.org/stable/user_guide.html#user-guide

# Tune models

## Hyperparameter tuning
### GridSearchCV
### RandomizedSearchCV 
* http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html

Examples:
* http://scikit-learn.org/stable/auto_examples/model_selection/plot_randomized_search.html
* https://www.programcreek.com/python/example/91146/sklearn.model_selection.RandomizedSearchCV
* https://stackoverflow.com/questions/35533253/how-would-you-do-randomizedsearchcv-with-votingclassifier-for-sklearn
* https://chrisalbon.com/machine_learning/model_selection/hyperparameter_tuning_using_random_search/

```python
# Import necessary modules
from scipy.stats import randint
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV

# Setup the parameters and distributions to sample from: param_dist
param_dist = {"max_depth": [3, None],
              "max_features": randint(1, 9),
              "min_samples_leaf": randint(1, 9),
              "criterion": ["gini", "entropy"]}

# Instantiate a Decision Tree classifier: tree
tree = DecisionTreeClassifier()

# Instantiate the RandomizedSearchCV object: tree_cv
tree_cv = RandomizedSearchCV(tree, param_dist, cv=5)

# Fit it to the data
tree_cv.fit(X, y)

# Print the tuned parameters and score
print("Tuned Decision Tree Parameters: {}".format(tree_cv.best_params_))
print("Best score is {}".format(tree_cv.best_score_))
```
[Source](https://campus.datacamp.com/courses/supervised-learning-with-scikit-learn/fine-tuning-your-model?ex=11#skiponboarding)


## Evaluate performance
### Scoring
* Accuracy
* Confusion matrix
* Precision and recall
* F1

* MSE
* RMSE
* R2

* Standard deviation

### Graph performance

Call backs
TensorBoard

## Predictions

# Prepare final model

# Final results

# Environment
`n_jobs = -1` means that the computation will be dispatched on all the CPUs of the computer.
http://scikit-learn.org/stable/tutorial/statistical_inference/model_selection.html

Running a process remotely
https://www.tecmint.com/keep-remote-ssh-sessions-running-after-disconnection/
https://www.tecmint.com/tmux-to-access-multiple-linux-terminals-inside-a-single-console/


