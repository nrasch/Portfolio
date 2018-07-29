# Clean up our environment
rm(list=ls(all=TRUE))

# Set seed so our results can be reproduced
set.seed(10)

# Load R libraries
library(coop)

# Load data
setwd("SOME_PATH_ON_YOUR_SYSTEM")
movies = read.csv("../RS2-Memory-Based-Recommendations-Jan-2018/data/movies.csv")
userMatrix = as.matrix(read.table("../RS2-Memory-Based-Recommendations-Jan-2018/data/userMatrix.txt", as.is = TRUE))
colnames(userMatrix) = seq(1, dim(userMatrix)[2], 1)

# Flip the matrix to an n-by-m format, where n = users and m = items
userMatrix = t(userMatrix)

#######################################
# 4.1.1.1 Cosine-Based Similarity Rev 1
buildModelCS.rev1 = function(R, k) {
  # Calc the number of items in R
  m = ncol(R)   
  
  # Init matrix to be returned by function
  M = matrix(data = 0, nrow = m, ncol = m)
  
  # Ensure k isn't greater than the number of items in R
  if (m < k) {
    k = m
  }
  
  for (j in 1:m) {
    for (i in 1:m) {
      if (i != j) {
        M[i,j] = cosineDist(R[, j], R[, i])    
      } 
    }
  }   # end for (j in 1:m) loop
  
  # Deal with any NaN/NA values in the user-item matrix
  M[is.na(M)] = 0
  
  for (j in 1:m) {
    
    # Scale the similarities to improve top-N recommendation quality
    M[,j] = M[,j] / sum(M[,j], na.rm = TRUE)
    
    #if M(i,j) != among the k largest values in M(*,j) then M(i,j) = 0
    kLargestIndex = (sort(M[,j], decreasing = TRUE, index.return = TRUE)$ix)[1:k]
    M[,j][-kLargestIndex] = 0
  } 

  return(M)
}

cosineDist <- function(vector1, vector2){
  return( sum(vector1 %*% vector2) / sqrt(sum(vector1^2) * sum(vector2^2)) )
}

# Testing and time to execute  measurements
dataSlice = userMatrix[1:300,1:3000]
start_time <- Sys.time()
model = buildModelCS.rev1(dataSlice, 15)
end_time <- Sys.time()
end_time - start_time
(sort(model[,1], decreasing = TRUE, index.return = TRUE)$ix)[1:10]
fix(model)


#######################################
# 4.1.1.1 Cosine-Based Similarity Rev 2
buildModelCS.rev2 = function(R, k) {
  # Calc the number of items in R
  m = ncol(R)   
  
  # Ensure k isn't greater than the number of items in R
  if (m < k) {
    k = m
  }
  
  M = coop::cosine(R)
  diag(M) = 0
  
  # Deal with any NaN/NA values in the user-item matrix
  M[is.na(M)] = 0

  for (j in 1:m) {
    # Scale the similarities to improve top-N recommendation quality
    M[,j] = M[,j] / sum(M[,j], na.rm = TRUE)

    #if M(i,j) != among the k largest values in M(*,j) then M(i,j) = 0
    kLargestIndex = (sort(M[,j], decreasing = TRUE, index.return = TRUE)$ix)[1:k]
    M[,j][-kLargestIndex] = 0
  }   # end for (j in 1:m) loop

  return(M)
  
}   # end function

# Testing and time to execute measurements
dataSlice = userMatrix[1:300,1:3000]
start_time <- Sys.time()
fasterModel = buildModelCS.rev2(dataSlice, 15)
end_time <- Sys.time()
end_time - start_time
(sort(fasterModel[,1], decreasing = TRUE, index.return = TRUE)$ix)[1:10]
fix(fasterModel)


#######################################
# Helper Functions

applyModel = function(M, U, N) {
  # The active user's information in vector U  is encoded by setting Ui = 1 if the
  # user has purchased the ith item and zero otherwise.
  U[U > 0] = 1
  
  # Deal with any NaN/NA values in the model 
  M[is.na(M)] = 0
  
  # First, the vector x is computed by
  # multiplying M with U (line 1). Note that the nonzero entries of x correspond
  # to the union of the k most similar items for each item that has already been
  # purchased by the active user, and that the weight of these entries is nothing
  # more than the sum of these similarities.
  x = M %*% U
  
  # Second, the entries of x that correspond
  # to items that have already been purchased by the active user are set to zero
  x[which(U != 0)] = 0
  
  # Finally, in the third step, the algorithm sets to zero all the entries of
  # x that have a value smaller than the N largest values of x
  x = (sort(x, decreasing = TRUE, index.return = TRUE)$ix)[1:N]

  return(x)
}


# Let's also create a helper function to show us which movies a particular user has rated
showUserRated = function(userMatrix, userIndex, movies) {
  userMatrix = t(userMatrix)
  rated = row.names(userMatrix[(which( userMatrix[, userIndex] != 0 )), ])
  rated = movies[ which (movies$movieId %in% rated), ]
  rated$rating = userMatrix[(which( userMatrix[, userIndex] != 0 )), ][, userIndex]
  rated = rated[with(rated, order(-rating)), ]
  
  return( rated[which(rated$rating >= 3),] )
}



#######################################
# Apply the Model

# OK, now let's apply the model and make some recommendations!

# Intialize parameters for use in the models
# Fortunately, as our experimental evaluation will illustrate (Section 6.2.1), reasonably small values of k
# (10 ??? k ??? 30) lead to good results and higher values lead to either a very small or no improvement.
k = 20
alpha = .5
numToRecco = 10
data = userMatrix[1:10,1:500]

## buildModelCS.rev1
# We know that the model "buildModelCS.rev1" is SLOW, so we're goign to skip it.


## buildModelCS.rev2
# We'll examine the 2nd revision of the cosine similarity model first (i.e. model "buildModelCS.rev2")

# Create the model
model.cs.rev2 = buildModelCS.rev2(userMatrix, k)

# Show current rantings for user 1 
showUserRated(userMatrix, 1, movies)

#      movieId                                          title                           genres rating
# 932     1172 Cinema Paradiso (Nuovo cinema Paradiso) (1989)                            Drama    4.0
# 1516    1953                  French Connection, The (1971)            Action|Crime|Thriller    4.0
# 1666    2105                                    Tron (1982)          Action|Adventure|Sci-Fi    4.0
# 1084    1339         Dracula (Bram Stoker's Dracula) (1992)  Fantasy|Horror|Romance|Thriller    3.5
# 834     1029                                   Dumbo (1941) Animation|Children|Drama|Musical    3.0
# 860     1061                                Sleepers (1996)                         Thriller    3.0
# 1709    2150                 Gods Must Be Crazy, The (1980)                 Adventure|Comedy    3.0
# 2926    3671                         Blazing Saddles (1974)                   Comedy|Western    3.0

# Examine the predictions for user 1
topItems = applyModel(model.cs.rev2, userMatrix[1,], numToRecco); movies[topItems, ]
#      movieId                                  title                             genres
# 2397    2985                         RoboCop (1987) Action|Crime|Drama|Sci-Fi|Thriller
# 971     1214                           Alien (1979)                      Horror|Sci-Fi
# 1115    1374 Star Trek II: The Wrath of Khan (1982)   Action|Adventure|Sci-Fi|Thriller
# 1021    1266                      Unforgiven (1992)                      Drama|Western
# 2175    2717                 Ghostbusters II (1989)              Comedy|Fantasy|Sci-Fi
# 2116    2641                     Superman II (1980)                      Action|Sci-Fi
# 2186    2728                       Spartacus (1960)           Action|Drama|Romance|War
# 1699    2140               Dark Crystal, The (1982)                  Adventure|Fantasy
# 2779    3479                       Ladyhawke (1985)          Adventure|Fantasy|Romance
# 1698    2139             Secret of NIMH, The (1982) Adventure|Animation|Children|Drama


# And how about for user 14?
showUserRated(userMatrix, 14, movies)
#      movieId                                                     title                                      genres rating
# 2553    3175                                       Galaxy Quest (1999)                     Adventure|Comedy|Sci-Fi      5
# 954     1196     Star Wars: Episode V - The Empire Strikes Back (1980)                     Action|Adventure|Sci-Fi      4
# 2507    3114                                        Toy Story 2 (1999) Adventure|Animation|Children|Comedy|Fantasy      4
# 3001    3751                                        Chicken Run (2000)                   Animation|Children|Comedy      4
# 3193    3988 How the Grinch Stole Christmas (a.k.a. The Grinch) (2000)                     Children|Comedy|Fantasy      4
# 1360    1721                                            Titanic (1997)                               Drama|Romance      3
# 1600    2038                          Cat from Outer Space, The (1978)                      Children|Comedy|Sci-Fi      3
# 1905    2394                               Prince of Egypt, The (1998)                           Animation|Musical      3
# 2104    2628          Star Wars: Episode I - The Phantom Menace (1999)                     Action|Adventure|Sci-Fi      3
# 2174    2716                Ghostbusters (a.k.a. Ghost Busters) (1984)                        Action|Comedy|Sci-Fi      3
# 2182    2724                                      Runaway Bride (1999)                              Comedy|Romance      3
# 2682    3354                                    Mission to Mars (2000)                                      Sci-Fi      3
# 2894    3623                             Mission: Impossible II (2000)                   Action|Adventure|Thriller      3
# 3191    3986                                       6th Day, The (2000)                      Action|Sci-Fi|Thriller      3

topItems = applyModel(model.cs.rev2, userMatrix[14,], numToRecco); movies[topItems, ]
#      movieId                                     title                                                    genres
# 1020    1265                      Groundhog Day (1993)                                    Comedy|Fantasy|Romance
# 1254    1580          Men in Black (a.k.a. MIB) (1997)                                      Action|Comedy|Sci-Fi
# 2399    2987           Who Framed Roger Rabbit? (1988) Adventure|Animation|Children|Comedy|Crime|Fantasy|Mystery
# 1025    1270                 Back to the Future (1985)                                   Adventure|Comedy|Sci-Fi
# 2213    2762                   Sixth Sense, The (1999)                                      Drama|Horror|Mystery
# 2242    2797                                Big (1988)                              Comedy|Drama|Fantasy|Romance
# 2063    2571                        Matrix, The (1999)                                    Action|Sci-Fi|Thriller
# 1046    1291 Indiana Jones and the Last Crusade (1989)                                          Action|Adventure
# 2250    2805                   Mickey Blue Eyes (1999)                                            Comedy|Romance
# 889     1097         E.T. the Extra-Terrestrial (1982)                                     Children|Drama|Sci-Fi

