function [] = main()
  
  % Close any graphs we have open from other processes
  close all;
  
  % Load our sample data set
  data = load('dataSet.txt');

  % Split our data up into x and y variables, so we can work with it easier later on
  % x contains rows of two data points, x1 and x2
  x = data(:, [1, 2]); 
  x1 = x(:,1);
  x2 = x(:,2);
  % y contains a binary classification [0|1] for each set of explanatory variables, x1 and x2
  y = data(:, 3);
  
  % Let's examine our sample data set (which upon visual inspection is clearly non-linear)
  plotData(x, y);
  fprintf('\nProgram paused. Press enter to continue.\n');
  pause;
  
  % Perform the regularized logistic regression to formulate our model
  
  % Since our data set is non-linear we'll need to add additional features to come up with a good model
  % In this case we'll add polynomial features up to degree six
  degree = 6;
  
  % Create our new polynomial feature matrix including a bias unit
  % x1, x2, x1.^2, x2.^2, x1*x2, x1*x2.^2, etc..
  X = mapFeature(x1, x2, degree);
 
  % Initialize fitting parameters
  initTheta = zeros(size(X, 2), 1);
  
  % Set fminunc options
  options = optimset('GradObj', 'on', 'MaxIter', 400);

  % Set regularization parameter lambda to 1
  lambda = 1;
  
  % Calculate optimal values of theta
  [theta, J, exit_flag] = fminunc(@(t)(costFunction(t, X, y, lambda)), initTheta, options);
   
  % Plot optimized non-linear decision boundary
  % The fourth parameter, 50 in this case, will control how many points to utilize
  % when drawing the decision boundary.  The greater the value the smoother the line
  % will be drawn.
  figure(1);
  plotDecisionBoundary(theta, X, y, 50, degree);
  testModel(theta, degree);
   
  % Compute accuracy on our training set
  p = predict(theta, X);
  fprintf('\nTrain Accuracy: %f  (lamba = %f)\n', mean(double(p == y)) * 100, lambda);

end


% A simple function to plot two values against each other on a graph, and visually
% indicate if the value has a Y value of one or zero
function plotData(x, y)
  hold on;

  % Calculate the index positions for each of the response variable classifications [0|1]
  pos = find(y==1);
  neg = find(y==0);

  % Place the non-linear data points into the graph and adjust the axis
  plot(x(pos,1), x(pos,2), 'rx', 'LineWidth', 2, 'MarkerSize', 4);
  plot(x(neg,1), x(neg,2), 'k*', 'LineWidth', 2, 'MarkerSize', 4);
  axis([-1.5 1.5 -1.5 1.5]);

  hold off;
end


%%%%
% WARNING
% There is much magic hand waving going on in the function below,
% so I have endeavoured to explain each step via the comments...
%%%%
function plotDecisionBoundary(theta, X, y, gridSize, degree)
  % Plot the data set minus the polynomial features we added
  plotData(X(:,2:3), y);
  
  hold on;

  % Set the grid range for the contour function below
  %
  % Linspace = Return a row vector with n linearly spaced elements between base and limit
  %
  % Gridsize controls how many predictions we'll be making using the optimized theta
  % and thus how many points we'll use to draw the contour plot
  % which in turn dictates how "smooth" of a line the contour line will depict
  %
  % Ex:  gridSize = 50 ==> u and v are set to values starting from -1 and ending 
  % at 1.5 in 50 incremental steps, which would give us a very smooth contour line
  %
  % The -1 and 2.5 values simply set the X,Y axis offsets of the grid we'll be viewing
  % and we pass them into the contour function below as such
  u = linspace(-1, 2, gridSize);
  v = linspace(-1, 2, gridSize);

  z = zeros(length(u), length(v));
  % Evaluate z = theta*x over the grid, where x = [u(i),v(j)]
  for i = 1:length(u)
    for j = 1:length(v)     
      % mapFeature creates a feature matrix including the bias unit, and returns
      % a matrix of dimension 1x28 that equals theta' dimensions (i.e. 28x1)
      %
      % z is then multiplied by theta to obtain the decision boundary values that
      % we can plot on the graph
      z(i,j) = mapFeature(u(i), v(j), degree)*theta;
    end
  end

  % Need to transpose z before calling contour
  z = z'; 

  % Create our contour plot (i.e. the decision boundary for our model)
  contour(u, v, z, [0, 0], 'LineWidth', 2)

  hold off
end


% Create a polynomial feature matrix including a bias unit
% x1, x2, x1.^2, x2.^2, x1*x2, x1*x2.^2, etc..
function output = mapFeature(x1, x2, degree)
  output = ones(size(x1(:,1)));
  for i = 1:degree
      for j = 0:i
          output(:, end+1) = (x1.^(i-j)).*(x2.^j);
      end
  end
end


%Predict whether the label is 0 or 1 using given theta values
function p = predict(theta, x)
  % Populate the return value
  m = size(x, 1);
  p = zeros(m, 1);
  
  % Apply the sigmoid function
  sigVal = 1 ./ (1 + exp(-(x*theta)));

  % Calculate the label classification/value
  p = sigVal >= 0.5;
end


% Compute the cost and gradient for logistic regression with regularization
% (This function is passed to "fminunc" as a parameter in the main script)
function [J, grad] = costFunction(theta, X, y, lambda)
  % Initialize variables
  m = length(y);
  J = 0;
  grad = zeros(size(theta));

  % Remove the bias unit
  newTheta = theta(2:end);
  
  % Apply the sigmoid function
  hTheta = 1 ./ (1 + exp(-(X*theta)));

  % Calculate regularized cost
  penalty = (lambda/(2*m)) * sum(newTheta .^ 2); 
  J = (1/m) * sum( (-y.*log(hTheta)) - (1-y).*(log(1-hTheta)) ) + penalty;

  % Calculate the regularized gradient of the cost
  grad = (1/m) * sum(( hTheta-y) .* X);
  % (Apply regularization to everything but parameter theta(0))
  grad(:,2:length(grad)) = grad(:,2:length(grad)) + (lambda/m)*newTheta';
end


% Plot a set of values so that we can visually inspect if they are within
% the decision boundary or not.  Then utilize our model to predict a classification
% for each value, and compare that against our visual inspection
function testModel(theta, degree)
  hold on;
  
  % Initialize variables
  a = [-1, -.5, 0, .5, 1];
  b = [-1, -.5, 0, .5, 1];
  aOffset = 0.15;
  bOffset = 0.15;
  
  for i = 1:length(a)
    % Draw data point on the graph
    plot(a(i), b(i), 'b+', "markersize", 12);
    % Create an annotation for the data point and place on the graph
    label = [ "(", num2str(a(i)) ", " num2str(b(i)), ")"];
    text(a(i)-aOffset, b(i)-bOffset, label, "fontsize", 12);
    % Use our model to make a prediction and return the results
    p = predict(theta, mapFeature(a(i), b(i), degree));
    fprintf('Label %s classified as %f\n', label, p);
  end
  
  fprintf('\n', label, p);
  
  hold off;
end