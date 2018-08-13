## Problem Setup

# Allow those following along to achieve the same results when running the code...
set.seed(10)

# Remove all objects except for functions in the environment
rm(list = setdiff(ls(), lsf.str()))

# Load up our data set
library(MASS)
attach(Boston)


###
# DATA EXPLORATION
###

# Columns in the data
names(Boston)

# Number of rows
nrow(Boston)

# How many missing values do we have
sapply(Boston,function(x) sum(is.na(x)))

# If we wanted a graphical representation of the missing values:
library(Amelia)
missmap(Boston, main = "Missing Values vs. Observed")

# How many unique values do we have for each column
sapply(Boston, function(x) length(unique(x)))

# Summary of the overall data set
summary(Boston)

# Record the "crim" median for use later on
crimMeadian = 0.25651

barplot(Boston$crim, main="Boston Per capita Crime Rate by Town", xlab="Town", ylab="Crime Rate")

###
# ADD RESPONSE VARABLE
###

# Create a variable to hold categorical assignments; set initial values to "No"  
Boston$crimRating = "No"

# Assign "Yes" to anything greater than the crim median
# Reminder:  We are using median due to the left skewed nature of the "crim" variable
Boston$crimRating[Boston$crim > median(Boston$crim)] = "Yes"

# The function "factor" is used to encode a vector as a factor; do this to utilize "crimRating" as a categorical variable
Boston$crimRating = factor(Boston$crimRating)

# Confirm the addition
is.factor(Boston$crimRating)
contrasts(Boston$crimRating)

# Visually inspect the results and drop the "crim" column
table(Boston$crimRating)
Boston = Boston[-drop(1)]

# And finally, what percentage of our data points are categorized as "No"
sum(Boston$crimRating=="No") / nrow(Boston) * 100
#[1] 50


###
# CREATE TRAINING AND TEST SETS
###

# We'll utilize 75% of the samples for the training set
trainIndex = sample(nrow(Boston), floor(nrow(Boston)*.75))
train = Boston[trainIndex,]
test = Boston[-trainIndex,]

# Confirm data set assignments (should equal zero)
nrow(train) + nrow(test) - nrow(Boston)


###
# MODEL FITTING - LOGISTIC REGRESSION
###

# Create a logistic regression model
model = glm(crimRating~., data=train, family=binomial)
summary(model)

# Cacluate the accuracy rating of the model
pre = predict(model, test, type="response")
result = rep("No", length(pre))
result[pre > crimMeadian] = "Yes"
table(result, test$crimRating)
mean(result==test$crimRating) * 100

# And what if we simplify the model by only utilizing those variables with a small z value as given by the "summary" command?
model = glm(crimRating ~ +zn +nox +dis +rad +tax +ptratio +medv, data=train, family=binomial)
summary(model)
pre = predict(model, test, type="response")
result = rep("No", length(pre))
result[pre > crimMeadian] = "Yes"
table(result, test$crimRating)
mean(result==test$crimRating) * 100

# Just as a sanity check let's assess our two models utilizing k-Fold Cross-Validation where k = 10:
library(boot)
model = glm(crimRating~., data=train, family=binomial)
1 - cv.glm(train, model, K=10)$delta[1]

model = glm(crimRating ~ +zn +nox +dis +rad +tax +ptratio +medv, data=train, family=binomial)
1 - cv.glm(train, model, K=10)$delta[1]


# The ROC curve and AUC also look solid:
library(ROCR)
pred = prediction(pre, test$crimRating)
prf = performance(pred, measure = "tpr", x.measure = "fpr")
plot(prf)

auc = performance(pred, measure = "auc")
auc = auc@y.values[[1]]
auc


###
# MODEL FITTING - KNN
###

# Load the "knn" library
library(class)

# Assign the train and test data to variables we can pass to the knn function as parameters
kTrain = cbind(train$zn, train$nox, train$dis, train$rad, train$tax, train$ptratio, train$medv)
kTest = cbind(test$zn, test$nox, test$dis, test$rad, test$tax, test$ptratio, test$medv)
kTrain.crimRating = train$crimRating

# Run model with k=1
k = 1
knnPre = knn(kTrain, kTest, kTrain.crimRating, k)
mean(knnPre==test$crimRating) * 100

# Run model with k=3
k = 3; knnPre = knn(kTrain, kTest, kTrain.crimRating, k); mean(knnPre==test$crimRating) * 100

# Run model with k=5
k = 5; knnPre = knn(kTrain, kTest, kTrain.crimRating, k); mean(knnPre==test$crimRating) * 100


# It appears that k=1 is our best bet, but let's confirm with cross-validation
# Note:  We'll utilize the caret package to make this easier on ourselves...
library(caret)

# Tell caret we want to examine k values from 1 to 15
tuneControl = expand.grid(.k=1:15)

# Setup the k-Fold Cross-Validation where k = 10 and we repeat the process 5 times
fitControl = trainControl(method = "repeatedcv", number = 10, repeats = 5)

# Let caret find the best model
knnFit = train(crimRating ~ +zn +nox +dis +rad +tax +ptratio +medv, data = train,
               method = "knn", 
               trControl = fitControl,
               tuneGrid = tuneControl, 
               preProcess = c("center","scale")
)

# Examine the results
knnFit

plot(knnFit)

confusionMatrix(predict(knnFit, test[,-14]), test$crimRating)


# Without k-Fold Cross-Validation:
k = 1
knnPre = knn(kTrain, kTest, kTrain.crimRating, k)
pre = prediction(c(knnPre), test$crimRating)
perf = performance(pre, measure = "tpr", x.measure = "fpr")
plot(perf)

auc = performance(pre, measure = "auc")
auc = auc@y.values[[1]]
auc

# (Note:  The caret package uses the "pROC" package for ROC/AUC calculations, so we need to do some conversion
# to make everything work with ROCR package we used earlier...)

# Use the KNN model created with caret to make predictions of the test set
vals = predict(knnFit, test[,-14])
# Convert the caret prediction set into a ROCR prediction object
pre2 = prediction(c(vals), test$crimRating)
# Now we can proceed as before using ROCR
perf2 = performance(pre2, measure = "tpr", x.measure = "fpr")
plot(perf2)

auc2 = performance(pre2, measure = "auc")
auc2@y.values[[1]]

# And, as a bonus for anyone worried about converting from caret/pROC to ROCR containing logic errors:

# Double-check our work above utilizing caret and the pROC library
pre3 = predict(knnFit, test[,-14], type='prob')
auc3 = roc(ifelse(test[,14]=="Yes",1,0), pre3[[2]])
plot(auc3)

auc3


###
# MODEL FITTING - RANDOM FOREST
###

library( randomForest)
rForest = randomForest(crimRating~., data=train, importance=TRUE)
varImpPlot(rForest)
pre = predict(rForest, test, type="response")
table(pre, test$crimRating)
mean(pre==test$crimRating) * 100
#[1] 93.70079

rForest = randomForest(crimRating ~ +zn +nox +dis +rad +tax +ptratio +medv, data=train, importance=TRUE, mtry=4)
varImpPlot(rForest)
pre = predict(rForest, test, type="response")
table(pre, test$crimRating)
mean(pre==test$crimRating) * 100
#[1] 93.70079


# And again let's confirm utilizing k-Fold Cross-Validation where k = 10 and we repeat the process 5 times
rForest = train(y=train$crimRating, x=train[,-14], trControl = fitControl, preProcess = c("center","scale"))
rForest


confusionMatrix(test$crimRating, predict(rForest, test[,-14]))

rForestData = train[,c("zn", "nox", "dis", "rad", "tax", "ptratio", "medv")]
rForest = train(y=train$crimRating, x=rForestData, trControl = fitControl, preProcess = c("center","scale"))
rForest


confusionMatrix(test$crimRating, predict(rForest, test[,-14]))

plot(rForest)


# Calculate the ROC and AUC to compare against the other models:
pre = predict(rForest, test[,-14], type='prob')
auc = roc(ifelse(test[,14]=="Yes",1,0), pre[[2]])
plot(auc)

auc


###
# MODEL FITTING - NEURAL NETWORK
###

# First let's define the settings we want caret to use when training the neural network model (NNM)
# Tell caret we want to examine k values from 1 to 15

# Setup the k-Fold Cross-Validation where k = 10 and we repeat the process 5 times
fitControl = trainControl(method = "repeatedcv", number = 10, repeats = 5)

# Set the tune parameters for the caret NNM
tuneControl = expand.grid(
  size = seq(from = 7, to = 28, by = 7), 
  decay = c(0.5, 0.1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7)
)

# Size is the number of units in the hidden layer; we'll go with 1,2,3, and 4 times the number of features
# Decay is the regularization parameter to avoid over-fitting

# Now let caret find the best model
nnm = train(crimRating ~ +zn +nox +dis +rad +tax +ptratio +medv, data = train, 
            method = "nnet", 
            trControl = fitControl,
            tuneGrid = tuneControl, 
            preProcess = c("center","scale")
)

# Note:  When utilizing a NNM we always want to center and scale the features to avoid the algorithm 
# failing to converge before the number of maximum iterations allowed is met



# Examine the results
nnm

confusionMatrix(predict(nnm, test[,-14]), test$crimRating)


# Let's try training the model again with all explanatory variables included:
nnm = train(crimRating ~., data = train,
            method = "nnet",
            trControl = fitControl,
            tuneGrid = tuneControl,
            preProcess = c("center","scale")
)

# Examine the results
nnm

confusionMatrix(predict(nnm, test[,-14]), test$crimRating)

plot(nnm)

# So a little less accurate utilizing all the explanatory variables of the Boston data set


# And finally, what if we let caret utilize random values for the size and decay?
# NOTE:  Fair warning, the command below can take a while to complete....
# And by "awhile" I mean like "I had time to go eat lunch and take a nap while it was working" kind of a while....
nnm = train(crimRating ~., data = train,
            method = "nnet",
            trControl = fitControl,
            tuneLength = 20,
            preProcess = c("center","scale")
)

# Examine the results
nnm

confusionMatrix(predict(nnm, test[,-14]), test$crimRating)

# So it appears that in addition to taking forever to compute letting caret utilize random values for tuning
# resulted in a model that fits less well than our previous two neural networks


# Let's go with the first NNM we tested, and take a look at the ROC and AUC for it:
nnm = train(crimRating ~ +zn +nox +dis +rad +tax +ptratio +medv, data = train, 
            method = "nnet", 
            trControl = fitControl,
            tuneGrid = tuneControl, 
            preProcess = c("center","scale")
)

pre = predict(nnm, test[,-14], type='prob')
auc = roc(ifelse(test[,14]=="Yes",1,0), pre[[2]])
plot(auc)

auc


###
# MODEL FITTING - SUPPORT VECTOR MACHINE
###

### SVM with linear kernel

# Setup the k-Fold Cross-Validation where k = 10 and we repeat the process 5 times
# Note we need to add the parameter "classProbs=TRUE", so that we can utilize pROC with this model later on
fitControl = trainControl(method = "repeatedcv", number = 10, repeats = 5, classProbs=TRUE)

# Configure and train the SVM model
# NOTE: We are reducing the tuneLength parameter to 10, as tuneLength = 20 was taking a very, very long time to complete
svm = train(crimRating ~ +zn +nox +dis +rad +tax +ptratio +medv, data = train, 
            method = "svmLinear2",    #utilizes the "e1071" library 
            trControl = fitControl,
            tuneLength = 10, 
            preProcess = c("center","scale")
)

# Examine the results
svm

confusionMatrix(predict(svm, test[,-14]), test$crimRating)

plot(svm)

# So the accuracy for the SVM model with a linear kernel is rather poor compared to previous models.  However, this does make sense,
# as one could imagine it's hard for the poor model to draw a straight line between seven different features. 

# And looking at the model's ROC graph and AUC value:

pre = predict(svm, test[,-14], type='prob')
auc = roc(ifelse(test[,14]=="Yes",1,0), pre[[2]])
plot(auc)

auc


### SVM with polynomial kernel

# Setup the k-Fold Cross-Validation where k = 10 and we repeat the process 1 time
fitControl = trainControl(method = "repeatedcv", number = 10, repeats = 5)

# Configure and train the SVM model
# NOTE:  We are setting the "tuneLength" parameter to 5, because 10+ is bogging down the author's poor laptop....   :(
svm = train(crimRating ~ +zn +nox +dis +rad +tax +ptratio +medv, data = train, 
            method = "svmPoly",
            trControl = fitControl,
            tuneLength = 5, 
            preProcess = c("center","scale")
)



# Examine the results
svm

confusionMatrix(predict(svm, test[,-14]), test$crimRating)

plot(svm)

# We have some improvement, but still less accuracy that previous models have produced.  Although the hyperplane created
# by the polynomial is more flexible than the linear model, it still isn't flexible enough to model our feature set with
# high accuracy.

# And looking at the model's ROC graph and AUC value:

vals = predict(svm, test[,-14])
pre = prediction(c(vals), test$crimRating)
perf = performance(pre, measure = "tpr", x.measure = "fpr")
auc = performance(pre, measure = "auc")
auc@y.values[[1]]

plot(perf, type="S")


### SVM with radial basis function (RBF) kernel

# Setup the k-Fold Cross-Validation where k = 10 and we repeat the process 5 times
fitControl = trainControl(method = "repeatedcv", number = 10, repeats = 5)

# Configure and train the SVM model
svm = train(crimRating ~ +zn +nox +dis +rad +tax +ptratio +medv, data = train, 
            method = "svmRadial",
            trControl = fitControl,
            tuneLength = 20, 
            preProcess = c("center","scale")
)

# Examine the results
svm

confusionMatrix(predict(svm, test[,-14]), test$crimRating)

# And looking at the model's ROC graph and AUC value:
vals = predict(svm, test[,-14])
pre = prediction(c(vals), test$crimRating)
perf = performance(pre, measure = "tpr", x.measure = "fpr")
auc = performance(pre, measure = "auc")
auc@y.values[[1]]

plot(perf, type="S")