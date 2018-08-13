## Machine Learning

## Implementations in Python
* [Python Development Environment Setup](./Python/P01-Python-Environment-Setup-Jan-2018)
* [Image Dataset Creation - Part One](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P02-Image-Dataset-Creation-Feb-2018/ImageDatasetCreation-PartOne.ipynb)
* [Image Dataset Creation - Part Two](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P02-Image-Dataset-Creation-Feb-2018/ImageDatasetCreation-PartTwo.ipynb)
* [Binary Image Classifier - Part Three](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P03-Image-Classifiers-Mar-2018/BinaryImageClassifier-PartThree.ipynb)
* [Binary Image Classifier - Part Four](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P03-Image-Classifiers-Mar-2018/BinaryImageClassifier-PartFour.ipynb)
* [Binary Image Classifier - Part Five](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P03-Image-Classifiers-Mar-2018/BinaryImageClassifier-PartFive.ipynb)
* [Binary Image Classifier - Part Six](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P03-Image-Classifiers-Mar-2018/BinaryImageClassifier-PartSix.ipynb)

## Implementations in R (and some Octave)
* [Basic Graphing Examples (1,952 words)](./R/Basic-Graphing-Nov-2017)
* [Basic Linear Regression (1,829 words)](./R/Basic-Linear-Regression-Nov-2017)
* [Basic Logistic Regression (1,158 words)](./R/Basic-Logistic-Regression-Nov-2017)
* [Logistic Models Comparison (5,679 words)](./R/Logistic-Models-Comparison-Dec-2017)
* Recommender Systems
  * [Introduction and Overview (2,307 words)](./R/RS0-Recommender-Systems-Intro-Jan-2018)
  * [Content Based Recommendations (4,153 words)](./R/RS1-Content-Based-Recommendations-Dec-2017)
  * [Memory Based Recommendations (4,190 words)](./R/RS2-Memory-Based-Recommendations-Jan-2018)
  * [Item Based Recommendations (3,105 words)](./R/RS3-Item-Based-Recommendations-Jan-2018)

### What is “Machine Learning”?

First, what exactly is machine learning?  Well, according to Wikipedia:

*Machine learning gives computers the ability to learn without being explicitly programmed (Arthur Samuel, 1959).  It is a subfield of computer science.*

*The idea came from work in artificial intelligence.  Machine learning explores the study and construction of algorithms which can learn and make predictions on data.  Such algorithms follow programmed instructions, but can also make predictions or decisions based on data.  They build a model from sample inputs.*

*Machine learning is done where designing and programming explicit algorithms cannot be done. Examples include spam filtering, detection of network intruders or malicious insiders working toward a data breach, optical character recognition (OCR), search engines and computer vision.*

*<https://simple.wikipedia.org/wiki/Machine_learning>*

Additionally, machine learning (ML) usually has two principal areas of activity: Supervised learning and unsupervised learning.  Let’s review these areas in an attempt to flesh out and better understand concretely the definition above.

### Supervised Learning

In a nutshell supervised learning entails providing the computer with a number of inputs and known outputs, and then asking the computer to create a model than can make predictions about new inputs it hasn't seen before.  (Usually the more examples the computer is given the better the predictive model created will be.)

Example:  A nonprofit creates an educational training program to increase the employability of a hard-to-serve population.  The nonprofit collects various data points on each set of students that pass through the program, and then follows up to record post-graduation employment metrics.

In this example the inputs for supervised learning would be the training program curriculum, time spent in the classroom vs. hands-on labs, the student-to-teacher ratio, etc.

The outputs for the supervised learning would be the change in the student's post-graduation employment rate, salary, etc.

The goal of the supervised learning problem for this example would be to end up with a model that could predict how successful attendees of the program would be based the configuration of the inputs.  For example, if the student-to-teacher ratio and number of hands-on labs (i.e. inputs) were modified, what would the supervised learning model predict would be the impact on graduates of the program finding meaningful employment (i.e. the output)?  Which inputs could be altered to have the greatest, positive impact on the desired output? 

Next, supervised learning problems are often categorized into "regression" and "classification" problems.  

#### Regression

When dealing with regression we want to create a model that can predict what the output values (i.e. change in employment rate) would be based on the input values (i.e. student-to-teacher ratio).  

Example:  If we had a 20:1 student-to-teacher ratio what would be the predicted change in the employment rate for individuals completing our program?  What would happen if we modified the ratio to 10:1?

#### Classification

Classification on the other hand deals with creating a model that will output a categorical prediction based on input values.  

Example:  We create three categories for our students to gauge their post-program success rate:  High, Medium, and Low.  As we alter various facets of the program (i.e. student-to-teacher ratio) which kind of post-program success rate will our model predict for that program configuration?  High, medium, or low?

#### Summary

As a rule of thumb:  Regression provides a hard number (i.e. a 20% increase in employment) while classification returns a category (i.e. medium).

### Unsupervised Learning
In supervised learning we were able to show the computer many examples where we knew what the output looked like based on the various inputs.  We could then take any predictive model created by the computer and run our known data through it, and then compare the supervised learning's predictions against what actually happened and ensure sane results were being generated.

In contrast, unsupervised learning allows us to explore data where we don't have a known set of outputs.  We want to explore the data organically and look for structures that might exist.  The computer doesn't have a "right" answer for a prediction; it attempts to create relationships based on the values of the inputs. 

Example:  We want to create a new training program to increase the employability of a hard-to-serve population.  We have enough funds to create three different program tracks, and we have a dataset containing information about our potential student body.  (The dataset might include various metrics such as education level, scholastic scores, known trade skills, and so forth.)  We'd like to utilize unsupervised learning to look for natural groupings (also called "clusters") in the potential student population, and then tailor each of the three program tracks to a cluster found through the unsupervised learning process.

The unsupervised learning problem would be setup to analyze student metric data and output three clusters (which we would hope to match up to the three funded program tracks under development).  Perhaps one cluster seems to indicate we have a grouping of students with low reading and math scores, while another cluster indicates a grouping of individuals with trade skill backgrounds, and the third cluster might contain a grouping of some other demographical significant characteristic.

Once the unsupervised learning  model identified the student population clusters appropriate program tracks could be developed to target the groupings:  once to increase scholastic abilities for those with low reading and math scores, another track to focus on job finding and interviewing skills for the trade skill cluster of students, and so forth.

## Implementations in Python
* [Python Development Environment Setup](./Python/P01-Python-Environment-Setup-Jan-2018)
* [Image Dataset Creation - Part One](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P02-Image-Dataset-Creation-Feb-2018/ImageDatasetCreation-PartOne.ipynb)
* [Image Dataset Creation - Part Two](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P02-Image-Dataset-Creation-Feb-2018/ImageDatasetCreation-PartTwo.ipynb)
* [Binary Image Classifier - Part Three](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P03-Image-Classifiers-Mar-2018/BinaryImageClassifier-PartThree.ipynb)
* [Binary Image Classifier - Part Four](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P03-Image-Classifiers-Mar-2018/BinaryImageClassifier-PartFour.ipynb)
* [Binary Image Classifier - Part Five](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P03-Image-Classifiers-Mar-2018/BinaryImageClassifier-PartFive.ipynb)
* [Binary Image Classifier - Part Six](https://nbviewer.jupyter.org/github/nrasch/Portfolio/blob/master/Machine-Learning/Python/P03-Image-Classifiers-Mar-2018/BinaryImageClassifier-PartSix.ipynb)

## Implementations in R (and some Octave)
* [Basic Graphing Examples (1,952 words)](./R/Basic-Graphing-Nov-2017)
* [Basic Linear Regression (1,829 words)](./R/Basic-Linear-Regression-Nov-2017)
* [Basic Logistic Regression (1,158 words)](./R/Basic-Logistic-Regression-Nov-2017)
* [Logistic Models Comparison (5,679 words)](./R/Logistic-Models-Comparison-Dec-2017)
* Recommender Systems
  * [Introduction and Overview (2,307 words)](./R/RS0-Recommender-Systems-Intro-Jan-2018)
  * [Content Based Recommendations (4,153 words)](./R/RS1-Content-Based-Recommendations-Dec-2017)
  * [Memory Based Recommendations (4,190 words)](./R/RS2-Memory-Based-Recommendations-Jan-2018)
  * [Item Based Recommendations (3,105 words)](./R/RS3-Item-Based-Recommendations-Jan-2018)
