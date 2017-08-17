import numpy as np
import pandas as pd
 
import costFunc
import gradDescent

np.random.seed(42)

#Import mean-normalized ratings dataset

train = pd.read_csv('<path>')

print "Data imported"

#Set up useful variables

uniqueGames = train.columns()
uniqueUsers = train.index()

numGames = uniqueGames.size
numUsers = uniqueUsers.size
numFeatures = 10

#Generate random initialization for parameters

param_len = (numGames * numFeatures) + (numUsers * numFeatures)
params0 = np.random.random(param_len) / 10


#Minimize cost function using gradient descent
    
alpha = 0.00005
max_iters = 15000

solution = gradDescent.minimize(costFunc.cost, costFunc.gradient, \
                              params0, Y, R, numUsers, numGames, \
                              numFeatures, lam, alpha, max_iters)
save_solution = pd.DataFrame(solution)
save_solution.to_csv('solution.csv')
print 'Solution saved'

solution_import = pd.read_csv('solution.csv', sep = ',', index_col = 0)
solution = solution_import.values

X = np.reshape(solution[0:numGames*numFeatures], [numGames, numFeatures])
Theta = np.reshape(solution[numGames*numFeatures:len(solution)], \
                            [numUsers, numFeatures])

ests = pd.DataFrame(np.dot(X, Theta.T), index = uniqueGames, columns = uniqueUsers)







