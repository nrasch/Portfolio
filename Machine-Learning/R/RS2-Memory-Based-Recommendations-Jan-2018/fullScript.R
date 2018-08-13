# Clean up our environment
rm(list=ls(all=TRUE))

# Set seed so our results can be reproduced
set.seed(10)

# Load R libraries
library(ggplot2)

# Load the processed MovieLens dataset
# Assumes we have access to and can load the processed data files from the previous write-up
# (../Machine-Learning/RS1-Content-Based-Recommendations-Dec-2017)
setwd("SOME_PATH_ON_YOUR_SYSTEM")
movies = read.csv("./data/movies.csv")
genreMatrix = as.matrix(read.table("./data/genreMatrix.txt", as.is = TRUE))
userMatrix = as.matrix(read.table("./data/userMatrix.txt", as.is = TRUE))
colnames(userMatrix) = seq(1, dim(userMatrix)[2], 1)

# How dense is the dataset?

image(userMatrix, col=topo.colors(12), main="Ratings Matrix Density")

#In the image above areas in dark blue indicate no ratings for a particular movie have been given 
# by a user.  The dataset is clearly sparsely populated which will make it harder on our model
# to predict accurate recommendations.  You can read more about sparse matrices [here](https://en.wikipedia.org/wiki/Sparse_matrix).

# How are the ratings that we do have distributed over the 1-to-5 movie rating scale?

qplot(userMatrix[userMatrix > 0], binwidth = .5, main = "Ratings Distribution", xlab = "User Rating", ylab = "Count")
summary(userMatrix[userMatrix > 0])

#  Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#  0.500   3.000   4.000   3.543   4.000   5.000 

# The ratings given by the users are skewed to the left, and average out to around 3.5.

# Next, how are the mean ratings distributed across the movies?

means = rowMeans(userMatrix, na.rm = TRUE); 
qplot(
  means, binwidth = .3, main = "Movie Rating Mean Distribution", 
  xlab = "Movie Rating Means", ylab = "Number of Movies"
)

# So almost 2000 movies were rated 3.5 or 4 with much fewer numbers of movies receiving a 1 or 5 rating.

# And how active were the users in the dataset about rating movies?

library(matrixStats)
rated = colCounts(userMatrix)
qplot(rated[rated != 0], binwidth = 10, xlab = "Number of Movies Rated", ylab = "Number of Users", main = "Number of Movies Rated by Users")

# The graph shows that anything after about 50 movies rated really tapers off in regard to user input...  
# Almost 120 different users rated at least one movie, but barely any users at all rated more than 200 movies for example.


# In order to build a user-based recommendation system we want to do the following:

# * Select a particular user (which we'll refer to as U1)
# * Use some method to find a neighborhood of people having similar tastes in movies to U1
# * Choose a subset, K, from the neighborhood of the most similar users (or use them all potentially)
# * Aggregate the K-nearest neighbors' movie ratings
# * Return top N number of movies with the highest user-based score that the U1 hasn't seen before

# There are two popular similarity measures used when finding K-nearest neighbors in recommendation system:
# the Pearson correlation coefficient and the Cosine similarity.  In this write-up we'll utilize the Cosine similarity
# which is defined by this formula:

# ![COSINE-FORMULA](./images/COSINE-FORMULA.png)
#Image credit:  https://en.wikipedia.org/wiki/Cosine_similarity


# Let's get started!


# Before we begin on the larger MovieLens data let's work through things on a sample data set
# we've crafted to ensure we understand what is happening, and that our process is sound.

# Load up the sample data

sampleData = as.matrix(read.csv("./data/knnTesting.csv", header = TRUE, row.names = 1))
sampleData

#      m1 m2 m3 m4 m5 m6 m7 m8 m9 m10 sum
# u1   5  5  5  5  5  5  5  5  5   5  50
# u2   5  5  5  5  5  5  5  5  5   5  50
# u3   3  5  4  2  2  1  1  4  3   2  27
# u4   1  5  2  3  4  1  4  1  1   2  24
# u5   2  2  4  4  2  1  2  2  2   2  23
# u6   3  4  2  4  5  3  4  2  1   5  33
# u7   3  3  4  1  2  4  4  1  5   4  31
# u8   0  0  0  0  0  0  0  0  0   0   0
# u9   1  1  1  1  1  1  1  1  1   1  10
# u10  1  1  1  1  1  1  1  1  1   1  10


# This gives a data set of 10 user ratings for 10 movies.  While this data set isn't very realistic.  
# it does; however, make it easy to confirm if our process is working as we'd expect.

# For example, it's clear that users 1 and 2 are similar, and likewise users 9 and 10 are also similar.
# We'd also expect user 8 to be closer in similarity with users 9 and 10 rather than user 1, and users 
# 6 and 7 should fall closer to users 1 and 2 rather than users 9 and 10.  This is also borne out by the 
# values in the "sum" column which was added as an aid to intuition.

# Let's examine some code to verify our intuition of the sample data set:

# Load the FNN library  (https://cran.r-project.org/web/packages/FNN/)
library(FNN)

# Drop the sum column, which is present for intuition puposes only
sampleData = sampleData[,-11]

# Calculate the k-nearest neighbors for all points where k = 3
nearest = knn.index(sampleData, k=3)
nearest

#         [,1] [,2] [,3]
# [1,]    2    6    7
# [2,]    2    6    7
# [3,]    5    4    7
# [4,]    6    5    3
# [5,]    3   10    9
# [6,]    4    5    7
# [7,]    5    3    6
# [8,]    9   10    5
# [9,]    9    8    5
# [10,]   9    8    5

# So that lines up nicely with our intuition on how things should work based on our sample
# data set.  User 1 is a k-nearest neighbor (KNN) with users 2, 6, and 7, while user 10 is a KNN
# with users 9, 8, and 5.

# However, what if we didn't want to constrain ourselves to some value of K?  What if we wanted *all* 
# the users that were similar based on some threshold value?  In that case we could examine the cosine
# similarity distance calculations:

# Load the coop library (https://cran.r-project.org/web/packages/coop/)
library(coop)

# Transpose sampleData, because coop wants to calculate by columns
cosine(t(sampleData))

# u1        u2        u3        u4        u5        u6        u7  u8        u9       u10
# u1  1.0000000 1.0000000 0.9050421 0.8593378 0.9312428 0.9333810 0.9221944 NaN 1.0000000 1.0000000
# u2  1.0000000 1.0000000 0.9050421 0.8593378 0.9312428 0.9333810 0.9221944 NaN 1.0000000 1.0000000
# u3  0.9050421 0.9050421 1.0000000 0.7921394 0.8821723 0.7869155 0.8077013 NaN 0.9050421 0.9050421
# u4  0.8593378 0.8593378 0.7921394 1.0000000 0.8263473 0.9215928 0.7562612 NaN 0.8593378 0.8593378
# u5  0.9312428 0.9312428 0.8821723 0.8263473 1.0000000 0.8588975 0.8190394 NaN 0.9312428 0.9312428
# u6  0.9333810 0.9333810 0.7869155 0.9215928 0.8588975 1.0000000 0.8245782 NaN 0.9333810 0.9333810
# u7  0.9221944 0.9221944 0.8077013 0.7562612 0.8190394 0.8245782 1.0000000 NaN 0.9221944 0.9221944
# u8        NaN       NaN       NaN       NaN       NaN       NaN       NaN   1       NaN       NaN
# u9  1.0000000 1.0000000 0.9050421 0.8593378 0.9312428 0.9333810 0.9221944 NaN 1.0000000 1.0000000
# u10 1.0000000 1.0000000 0.9050421 0.8593378 0.9312428 0.9333810 0.9221944 NaN 1.0000000 1.0000000

# OK, this obviously isn't what we want.  According to coop's cosine similarity outputs users 1, 2, 9, and
# 10 would be grouped together as KNN.  Using user 9 and 10's ratings to make recommendations for user 1
# isn't going to result in optimal results; it's pretty clear that user 1 has complete opposite tastes
# in movies from users 9 and 10.

# If we reduce this to a 2 dimensional space and graph the vectors it becomes clear what is going on:

plot(x=c(0,4), y=c(0,4), pch=19, col="black", cex=1.5, type="b", xlab = "X", ylab= "Y", main="Vector Graph")
points(c(0,2), c(0,2), col="red", type="b", cex=1, pch=22, bg="red")
legend("numeratorleft", legend=c("Vec 1", "Vec 2"), col=c("black", "red"), lty=1, cex=1)


# ![VECTOR-GRAPH](./images/VECTOR-GRAPH.png)

# So the two vectors are laying on top of one another.  However, as seen below, the cosine similarity
# function is looking for the cosine of the angle between them, which is in this case is zero.

# ![COSINE-GRAPH](./images/COSINE-GRAPH.png)
#Image credit:  https://www.safaribooksonline.com

# We can also work out the math by hand to verify using the cosine similarity formula:

# ![COSINE-FORMULA](./images/COSINE-FORMULA.png)
#Image credit:  https://en.wikipedia.org/wiki/Cosine_similarity

v1 = sampleData[1,]
v2 = sampleData[2,]
v9 = sampleData[9,]

# User 1 and user 2
numerator = sum(v1 %*% v2)
denominator = sqrt( sum(v1)^2 ) %*% sqrt( sum(v2)^2 )
numerator/denominator
# [,1]
# [1,]  0.1

# User 1 and user 9
numerator = sum(v1 %*% v9)
denominator = sqrt( sum(v1)^2 ) %*% sqrt( sum(v9)^2 )
numerator/denominator
# [,1]
# [1,]  0.1

# To get around this we can do one of two things:  Calculate the distance between the vectors in Euclidean space,
# or convert sampleData to a binary matrix, and then compute the cosine similarity.

# Euclidean Space

# R already has a function that will compute this for us:
?dist
dist(sampleData)

# u1        u2        u3        u4        u5        u6        u7        u8        u9
# u2   0.000000                                                                                
# u3   8.306624  8.306624                                                                      
# u4   9.380832  9.380832  5.916080                                                            
# u5   9.000000  9.000000  4.472136  5.000000                                                  
# u6   6.708204  6.708204  6.928203  4.582576  6.000000                                        
# u7   7.280110  7.280110  6.324555  7.000000  6.164414  6.480741                              
# u8  15.811388 15.811388  9.433981  8.831761  7.810250 11.180340 10.630146                    
# u9  12.649111 12.649111  6.708204  6.324555  5.000000  8.306624  7.810250  3.162278          
# u10 12.649111 12.649111  6.708204  6.324555  5.000000  8.306624  7.810250  3.162278  0.000000

# Note that smaller values imply a greater similarity. 

# This is much more in line with what we wanted, and would accommodate using a threshold value to filter which
# users we would consider similar to our target user (i.e. only consider those users where the "dist" value was
# 8.0 or less as "similar" for example).

# Binary Matrix

# Convert the sampleData into a binary matrix
sampleDataBinary = sampleData
# We only want to consider ratings that were three or higher
sampleDataBinary[sampleData > 2] = 1
sampleDataBinary[sampleData <= 2] = 0
sampleDataBinary

#      m1 m2 m3 m4 m5 m6 m7 m8 m9 m10
# u1   1  1  1  1  1  1  1  1  1   1
# u2   1  1  1  1  1  1  1  1  1   1
# u3   1  1  1  0  0  0  0  1  1   0
# u4   0  1  0  1  1  0  1  0  0   0
# u5   0  0  1  1  0  0  0  0  0   0
# u6   1  1  0  1  1  1  1  0  0   1
# u7   1  1  1  0  0  1  1  0  1   1
# u8   0  0  0  0  0  0  0  0  0   0
# u9   0  0  0  0  0  0  0  0  0   0
# u10  0  0  0  0  0  0  0  0  0   0

# Let's try the coop::consine function again
coop::cosine(as.matrix(t(sampleDataBinary)))

#     u1        u2        u3        u4        u5        u6        u7        u8  u9  u10
# u1  1.0000000 1.0000000 0.7071068 0.6324555 0.4472136 0.8366600 0.8366600 NaN NaN NaN
# u2  1.0000000 1.0000000 0.7071068 0.6324555 0.4472136 0.8366600 0.8366600 NaN NaN NaN
# u3  0.7071068 0.7071068 1.0000000 0.2236068 0.3162278 0.3380617 0.6761234 NaN NaN NaN
# u4  0.6324555 0.6324555 0.2236068 1.0000000 0.3535534 0.7559289 0.3779645 NaN NaN NaN
# u5  0.4472136 0.4472136 0.3162278 0.3535534 1.0000000 0.2672612 0.2672612 NaN NaN NaN
# u6  0.8366600 0.8366600 0.3380617 0.7559289 0.2672612 1.0000000 0.7142857 NaN NaN NaN
# u7  0.8366600 0.8366600 0.6761234 0.3779645 0.2672612 0.7142857 1.0000000 NaN NaN NaN
# u8        NaN       NaN       NaN       NaN       NaN       NaN       NaN   1 NaN NaN
# u9        NaN       NaN       NaN       NaN       NaN       NaN       NaN NaN   1 NaN
# u10       NaN       NaN       NaN       NaN       NaN       NaN       NaN NaN NaN   1

# Note that larger values imply a greater similarity. 

# This now lines up with the KNN and Euclidean space outputs, and also accommodates filtering
# by a threshold value (i.e. only consider those users where the cosine similarity value is
# 8.0 or greater as "similar" for example).


# Predict recommendations

# Let's put everything together and predict a movie recommendation based on similar users.  
# We'll pick user 1 and predict if we should recommend movie 5 or not based on what 
# other users similar to user 1 rated the movie.  

# Note:  We'll utilize the "coop" package to make implementing weights easier during the process.

# Calculate cosine similarity using "coop" package, and pull out results for user 1
dist.u1 = (coop::cosine(as.matrix(t(sampleDataBinary))))[,c("u1")]
# Remove user 1 from the results, because we don't want to compare user 1 to themselves
dist.u1 = dist.u1[names(dist.u1) != "u1"]
# Remove NaN results
dist.u1 = na.omit(dist.u1)
# Collect the names of users similar to user 1
similarUsers = names(dist.u1[dist.u1 >= 0.8])

# Define the movie's index
movieIndex = 5
# Collect the ratings that users similar to user 1 gave movie 5 
ratings = sampleData[similarUsers, movieIndex]

# Calculate a recommendation rating for movie 5 using a simple average of ratings that users similar
# to user 1 gave movie 5

# ![RATING-FORMULA-1](./images/RATING-FORMULA-1)

ratingNonWeighted = sum(ratings)/length(ratings)
ratingNonWeighted
# [1] 4

# The result is a 4 which is realistic based on similar users giving movie 5 a rating set of [5,5,2].  In this
# case we would go ahead and recommend movie 5 to user 1 based on such the high prediction value.

# We can also calculate the predicted recommendation rating utilizing a weighted average where 
# the more similar a given user is to user 1 the more weight their rating receives:

# Collect the cosine similarity values which will be used as weights
weights = dist.u1[dist.u1 >= 0.8]

# Calculate the recommendation rating for movie 5 using a weighted average of ratings that users 
# similar to user 1 gave movie 5

# ![RATING-FORMULA-2](./images/RATING-FORMULA-2)

ratingWeighted = sum(weights * ratings) / sum(weights)
ratingWeighted
# [1] 4.0611

# The result is 4.0611 which again is realistic based on the similar users' ratings of movie 5.



# Next well create some functions to perform the work we just did "by hand" above, and then we can 
# use those functions on the much larger MovieLens data.


# Convert a given matrix of numerical values into binary form
# Values of the matrix >= the threshold parameter are set to one, otherwise zero
toBinary = function(matrix, threshold) {
  # Convert items less than the threshold to 0
  matrix[matrix < threshold] = 0
  
  # Convert items equal or greater than the threshold to 1
  matrix[matrix >= threshold] = 1
  
  
  return(matrix)
}

# Provides a quick summary and graph of the ratings that have been recorded for a particular movie.
# Excludes the ratings for a given user, so that the sparsity of a movie's ratings can
# be intuitively observed for similar user comparisons 
userMovieInfo = function(ratingMatrix, userColumnIndex, movieRowIndex) {
  
  m = paste("movie[", movieRowIndex, "]", sep="")
  u = paste("user[", userColumnIndex, "]", sep="")
  
  movieRatings = ratingMatrix[movieRowIndex, -userColumnIndex]
  txt = c(" There are", length(movieRatings), "possible ratings for", m, "\n")
  
  movieRatingsPopulated = movieRatings[movieRatings !=0]
  txt = c(txt, length(movieRatingsPopulated), "non-zero ratings have been recorded for", m, "\n")
  
  txt = c(txt, "   (Note that", u, "has been excluded from these counts)\n")
  txt = c(txt, "Drawing distribution graph of rating values for", m, "\n")
  
  cat(txt)
  
  qplot(movieRatingsPopulated, binwidth = 0.1, boundary = -0.05)
}

# Quick testing
userMovieInfo(userMatrix, 1, 5)
# There are 670 possible ratings for movie[5] 
# 56 non-zero ratings have been recorded for movie[5] 
# (Note that user[1] has been excluded from these counts)
# Drawing distribution graph of rating values for movie[5]
# ![userMovieInfo1](./images/userMovieInfo1.png)

userMovieInfo(userMatrix, 1, 932)
# There are 670 possible ratings for movie[932] 
# 45 non-zero ratings have been recorded for movie[932] 
# (Note that user[1] has been excluded from these counts)
# Drawing distribution graph of rating values for movie[932] 
# ![userMovieInfo2](./images/userMovieInfo2.png)


# Takes a given user's movie ratings and then uses cosine similarity to find other users
# who have similar movie rankings.
#
# @param ratingMatrix     A matrix with movie IDs as rows, user IDs as columns, and movie ratings as data points
# @param userIndex        The index of the user that other, similar users should be found for
# @param ratingLimit      Rating values equal to or greater than this value will count as a positive rating
# @param similarityLimit  Threshold value for determining which users are "similar" to the user in question
#
# Returns a list with three components:
# $userNames     The userIds of similar users
# $userWeights   The weights (i.e. distances) between similar users and the specified user
# $output        A narrative summarizing the results of the function's operations
similarUsers = function(ratingMatrix, userIndex, ratingLimit, similarityLimit) {
  similarUsers = list()
  u = paste("user[", userIndex, "]", sep="")
  
  txt = c(" Finding similar users for", u, "...\n")

  # Convert rating matrix to binary format (ratings >= ratingLimit = 1; else 0)
  ratingMatrixBinary = toBinary(ratingMatrix, ratingLimit)
  
  # Calculate cosine similarity using "coop" package, and pull out results for given user
  dist = coop::cosine(ratingMatrixBinary)[,userIndex]
  # Remove given user from the results, because we don't want to compare given user to themselves
  dist = dist[-userIndex]
  # Remove NaN results
  dist = na.omit(dist)
 
  # Collect the names of users similar to given user
  similarUsers$userNames = names(dist[dist >= similarityLimit])
  
  # Collect the cosine similarity values which will be used as weights
  similarUsers$userWeights = dist[dist >= similarityLimit]
  
  txt = c(txt, "The cosine similarity calculations found", length(similarUsers$userNames), "similar users for", u, "\n")
  txt = c(txt, "similar users:", similarUsers, "\n")
  txt = c(txt, "similar user weights:", round(weights, 2), "\n")
  
  similarUsers$output = txt
  
  return(similarUsers)
}

# Quick testing
test = similarUsers(userMatrix, 1, 3, 0.08)
names(test)
test$userNames
round(test$userWeights, 2)
cat(toString(test$output))

# Names:       "userNames"   "userWeights" "output"     
# $userNames:  "35"  "76"  "102" "207" "310" "325" "341" "387" "485" "510" "575" "594" "604" "634"
# $userWeights: 0.13 0.08 0.08 0.09 0.12 0.12 0.08 0.11 0.09 0.10 0.08 0.08 0.11 0.10 
# Finding similar users for, user[1], ...
# The cosine similarity calculations found, 14, similar users for, user[1], 
# Similar users:, c("35", "76", "102", "207", "310", "325", "341", "387", "485", "510", "575", "594", "604", "634"), c(0.133630620956212, 0.0811107105653813, 0.0845154254728517, 0.0883883476483184, 0.125, 0.125, 0.0811107105653813, 0.107384194896889, 0.0883883476483184, 0.098907071009368, 0.0841793787126842, 0.0845154254728517, 0.106600358177805, 0.102062072615966), 
# Similar user weights:, 1, 0.84, 0.84, 


# Calculates a predicted user-based recommendation score for a movie for a particular user-based
# on what similar users have rated that movie
#
# @param movieRow         The row of movie ratings from the userMatrix for a specified movie
# @param similarUsers    A vector of similar user Ids
# @param weights          A vector of similar user weights (i.e. cosine similarity distances)
#
# Returns a list with two components:
# $score      The predicted recommendation rating for a particular movie based on the weighted average of similar user ratings
# $output     A narrative summarizing the results of the function's operations
recommendationScore = function(movieRow, similarUsers, weights) {
  WeightedRatingScore = list()
  
  m = paste("movie[", movieIndex, "]", sep="")
  
  # Collect the ratings that users similar to given user gave given movie
  ratings = movieRow[similarUsers]
  txt = c(" Similar user ratings:", ratings, "\n")
  
  # Calculate the predicted recommendation rating utilizing a weighted average where 
  # the more similar a given user is to given user the more weight their rating receives:
  
  # Perform the weighted rating calculation
  WeightedRatingScore$score = sum(weights * ratings) / sum(weights)
  
  txt = c(txt, "The final user-based recommendation prediction rating for", m, "is", round(WeightedRatingScore$score, digits = 2), "\n")
  
  WeightedRatingScore$output = txt
  
  return(WeightedRatingScore)
}


# Quick testing 1 for a movie user 1 wouldn't like
score = recommendationScore(userMatrix[5, ], test$userNames, test$userWeights)
names(score)
score$score

# cat(toString(score$output))
# [1] "score"  "output"
# [1] 0
# Similar user ratings:, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
# , The final user-based recommendation prediction rating for, movie[5], is, 0,


# Quick testing 2 for a movie user 1 would like
score = recommendationScore(userMatrix[932, ], test$userNames, test$userWeights)
names(score)
score$score
cat(toString(score$output))

# [1] "score"  "output"
# [1] 1.397736
# Similar user ratings:, 0, 0, 4, 0, 0, 2, 4, 5, 0, 5, 0, 0, 0, 0, 
# , The final user-based recommendation prediction rating for, movie[5], is, 1.4,



# Now let's use the functions we just wrote to pick a user and find user-based recommendations
# from a pool of all unrated movies for that user and return a top 10 list of the highest scoring items.

# 1: As before, compile a list of similar users
  simUsers = similarUsers(userMatrix, 1, 3, 0.08)

# 2: Remove any movies that the user in question has already rated
  userRatings = userMatrix[-(which( userMatrix[, 1] != 0 )), ]

# 3: For each movie calculate a user-based recommendation prediction rating

  # Prepare a data.frame to record the results
  results = data.frame("movieId" = rownames(userRatings), "score" = 0)
  
  # Loop through each movie and record predicted user-based recommendation score
  for (id in 1:(nrow(results))) {
    score = recommendationScore(userMatrix[id, ], simUsers$userNames, simUsers$userWeights)
    results[id, "score"] = score$score
  }
  
  # Order the results in descending order, so we can pull the top 10
  results = results[with(results, order(-score)), ]

# 4: Return the top 10 entries along with movie details
  recommended = movies[ which(movies$movieId %in% results[1:10, ]$movieId), ]
  recommended$score = results[1:10, ]$score
  recommended$title = strtrim(recommended$title, 35)
  recommended
  
  #      movieId                               title                        genres    score
  # 286      319                Shallow Grave (1994)         Comedy|Drama|Thriller 1.838062
  # 537      609 Homeward Bound II: Lost in San Fran            Adventure|Children 1.520299
  # 628      753         Month by the Lake, A (1995)          Comedy|Drama|Romance 1.461845
  # 697      861 Supercop (Police Story 3: Supercop)  Action|Comedy|Crime|Thriller 1.459531
  # 937     1177              Enchanted April (1992)                 Drama|Romance 1.446037
  # 983     1226               Quiet Man, The (1952)                 Drama|Romance 1.409902
  # 991     1235             Harold and Maude (1971)          Comedy|Drama|Romance 1.397736
  # 1066    1320     Alien³ (a.k.a. Alien 3) (1992) Action|Horror|Sci-Fi|Thriller 1.360653
  # 1724    2168                Dance with Me (1998)                 Drama|Romance 1.360653
  # 2946    3691               Private School (1983)                        Comedy 1.348102

# 5: Examine the movies the selected user has previously rated at 3 or above
  rated = row.names(userMatrix[(which( userMatrix[, 1] != 0 )), ])
  rated = movies[ which (movies$movieId %in% rated), ]
  rated$rating = userMatrix[(which( userMatrix[, 1] != 0 )), ][, 1]
  rated = rated[with(rated, order(-rating)), ]
  rated[which(rated$rating >= 3),]
  
  #      movieId                                         title                            genres rating
  # 932     1172 Cinema Paradiso (Nuovo cinema Paradiso) (1989)                            Drama    4.0
  # 1516    1953                  French Connection, The (1971)            Action|Crime|Thriller    4.0
  # 1666    2105                                    Tron (1982)          Action|Adventure|Sci-Fi    4.0
  # 1084    1339         Dracula (Bram Stoker's Dracula) (1992)  Fantasy|Horror|Romance|Thriller    3.5
  # 834     1029                                   Dumbo (1941) Animation|Children|Drama|Musical    3.0
  # 860     1061                                Sleepers (1996)                         Thriller    3.0
  # 1709    2150                 Gods Must Be Crazy, The (1980)                 Adventure|Comedy    3.0
  # 2926    3671                         Blazing Saddles (1974)                   Comedy|Western    3.0
  
# If we compare the user's movie ratings by genre that we know about against what the model has selected as
# as a recommendation things look pretty good.   The only item I'm a little dubious about is the movie
# "Homeward Bound II: Lost in San Francisco (1996)" due to the genre label "Children." However, it would be
# fascinating to have the user watch this movie and then see how they rated it.  If they liked the movie then
# it would strengthen the relationship between the user and the similar users the model selected, and if they
# didn't like it then the model could adjust the similar user weights accordingly.
  
# And this brings us to one of the benefits of this model:  As the user base continues to add ratings for the 
# various movies the model will increase in accuracy  It will be able to "learn" more about what each user
# like/dislikes, and then find better and better similar user matches.  This in turn will increase the
# recommendation predictions the model can make for each user.
  
# This will also potentially expose the user to new movies they might not have selected for themselves otherwise.
# A great example is from the results we already have with the inclusion of the movie "Homeward Bound II: Lost 
# in San Francisco (1996)."  Based on the genres that the user has rated it doesn't appear this would be a 
# good match.  However, obviously enough users with similar tastes to our selected user did enjoy the movie,
# so there is definitely a chance our selected user might like it too.