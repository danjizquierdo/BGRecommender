#Runs gradient descent on collaborative filtering algorithm

import math

def minimize(f, fprime, x0, Y, R, num_users, num_samples, num_features, \
             lam, alpha, max_iters):
    costs = []
    solution = x0

    #Loop gradient descent
    for i in range(max_iters):
        cost = f(solution, Y, R, num_users, num_samples, num_features, lam)
        if math.isnan(cost):
            break
        if i % 25 == 0:
            costs.append(cost)
            print i, cost
        gradient = fprime(solution, Y, R, num_users, num_samples, num_features, lam)
        delta = alpha * gradient
        solution = solution - delta

    return solution
        
        
    
