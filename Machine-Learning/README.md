# Machine Learning

## Python

### Development environment setup

* [Development environment setup](./Python/01-ComputerVision-Environment-Setup)


### Computer vision - Data set creation

This set of write-ups covers creating a dataset of images suitable for use in future machine learning projects.

* [Image Dataset Creation - Part One](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/02-ComputerVision-Dataset-Creation/ImageDatasetCreation-PartOne.ipynb)
  
  * The objectives of this write-up include:
    * Find and acquire a suitable set of images
    * Process a small subset of images as a proof of concept for the image dataset creation process
    * Output a portable binary data container containing the subset of processed images

* [Image Dataset Creation - Part Two](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/02-ComputerVision-Dataset-Creation/ImageDatasetCreation-PartTwo.ipynb)

	* Implementation of the prototype and ideas developed in [part one](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/02-ComputerVision-Dataset-Creation/ImageDatasetCreation-PartOne.ipynb)

### Computer vision - Image classification

This set of write-ups covers creating image classification models from scratch, in TensforFlow, and in Keras.  The Jupyter notebooks for each model are listed below:

* [Basic logistic regression model from scratch](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/03-ComputerVision-Classification/Classification-01.ipynb)
* [Shallow neural network from scratch](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/03-ComputerVision-Classification/Classification-02.ipynb)
* [N-layer neural network from scratch](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/03-ComputerVision-Classification/Classification-03.ipynb)
* [N-layer neural network optimizations from scratch](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/03-ComputerVision-Classification/Classification-04.ipynb)
* [TensforFlow baseline](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/03-ComputerVision-Classification/Classification-05.ipynb)
* [Keras baseline](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/03-ComputerVision-Classification/Classification-06.ipynb)


### Reference models

A set of reference models (mostly in TensorFlow), that saves me a lot of time having to look these things up...  ;)

* [Base neural network](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/05-Reference-Models/DNN-TensorFlow-Base.ipynb) - A very basic 2 layer neural network [TensorFlow] 

* [Training deeper neural networks](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/05-Reference-Models/DNN-TensorFlow-Training.ipynb) - Implementations for training deeper neural networks [TensorFlow]
  - Vanishing/Exploding Gradients
  - Non-saturating Activation Functions
  - Transfer Learning
  - Optimizers
  - Regularization
  
* [TensorBoard](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/05-Reference-Models/DNN-TensorBoard.ipynb) - Implementing TensorBoard to understand, debug, and optimize TensorFlow models


### Classic data sets

This set of write-ups covers working through predictive modeling machine learning problems using classic datasets.  The Jupyter notebooks for each model are listed below:

* [Iris Classification](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-01.ipynb) - Classification with Scikit-Learn

* [Iris Classification with Keras](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-01.Keras.1.ipynb) - Neural network classification with Keras

* [Boston Housing Prices](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-02.ipynb) - Linear and non-linear algorithm regression modeling with Scikit-Learn

* [Boston Housing Prices with Keras](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-02.Keras.1.ipynb) - Neural network regression modeling with Keras and GridSearchCV

* [Boston Housing Prices with Keras](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-02.Keras.2.ipynb) - Neural network regression modeling with Keras and RandomizedSearchCV

* [Sonar, Mines vs. Rocks](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-03.ipynb) - Linear and non-linear algorithm regression modeling with Scikit-Learn

* [Student Alcohol Consumption](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-04.ipynb) - Linear and non-linear algorithm regression modeling with Scikit-Learn as well as a neural network implementation with TensorFlow

* [MNIST Image Classification](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-05.ipynb) - Image classification modeling with Long Short Term Memory (LSTM) networks and TensorFlow

* [IMDB Movie Review Sentiment Classification](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-06.ipynb) - Movie review classification modeling using natural language processing, Scikit-Learn, and bag-of-words

* [IMDB Movie Review Sentiment Classification](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-06.p2.ipynb) - Movie review classification modeling using natural language processing, Scikit-Learn, and bag-of-words on a sparse feature set

* [IMDB Movie Review Sentiment Classification](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/04-Classic-Datasets/Model-06.p3.ipynb) - Movie review classification modeling using natural language processing, Word2Vec, and Scikit-Learn on a feature set of centroids

## R (with some Octave)

* [Graphing and Basic Models](./R)
* Recommender Systems
    * [Intro & Overview](./R/RS0-Recommender-Systems-Intro-Jan-2018)
    * [Content Based](./R/RS1-Content-Based-Recommendations-Dec-2017)
    * [Memory Based](./R/RS2-Memory-Based-Recommendations-Jan-2018)
    * [Item Based](./R/RS3-Item-Based-Recommendations-Jan-2018)


## Other Items

### Works in Progress

* [Definitions](./General/Definitions/README.md)
* [Project Template - VERY rough draft](./General/Project-Template/README.md)
