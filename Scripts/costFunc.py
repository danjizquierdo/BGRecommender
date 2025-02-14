#Computes cost and gradient for input ratings and parameters
import numpy as np

#Needs to be edited to work wtih arrays where blanks are represented by nans
# instead of 0's (eliminating R matrix). Could be done by using numpy function
# to replace nan's with zeros inside this function or could be some other solution


def cost(params, Y, R, num_users, num_games, num_features, lam):
    #Unfold parameter matrix
    X = np.reshape(params[0:num_games*num_features], [num_games, num_features])
    Theta = np.reshape(params[num_games*num_features:len(params)], \
                            [num_users, num_features])
    
    #Set vars to return
    J = 0
    
    #Compute regularized cost
    estimates = np.dot(X, Theta.T)
    error = np.multiply(estimates, R) - np.multiply(Y, R)
    
    X_reg = lam * np.sum(np.square(X))
    Theta_reg = lam * np.sum(np.square(Theta))

    J = (np.sum(np.square(error)) + X_reg + Theta_reg) / 2

    return J
    
def gradient(params, Y, R, num_users, num_games, num_features, lam):
    #Unfold parameter matrix
    X = np.reshape(params[0:num_games*num_features], [num_games, num_features])
    Theta = np.reshape(params[num_games*num_features:len(params)], \
                            [num_users, num_features])
    
    #Set vars to return
    X_grad = np.zeros(X.shape)
    Theta_grad = np.zeros(Theta.shape)

    #Compute regularized cost and gradients
    estimates = np.dot(X, Theta.T)
    error = np.multiply(estimates, R) - np.multiply(Y, R)
    
    X_grad = np.dot(error, Theta) + lam * X
    Theta_grad = np.dot(error.T, X) + lam * Theta

    #Set up output
    grad = np.append(X_grad, Theta_grad)

    return grad
