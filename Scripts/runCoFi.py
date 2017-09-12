import numpy as np
import pandas as pd
 
import costFunc
import gradDescent
from normalize import mean_normalize

np.random.seed(42)

#Import mean-normalized ratings dataset
path = 'C:/python27/BGRec/'

rawInput = pd.read_csv(path+'Raw/Input.csv',index_col=0)
train,normal = mean_normalize(rawInput)
#normal.to_csv(path+'Output/averages.csv')
#train.to_csv(path+'Output/trainingset.csv')

print "Data imported"

#Set up useful variables

uniqueGames = train.columns
uniqueUsers = train.index

numGames = uniqueGames.size
numUsers = uniqueUsers.size
numFeatures = 10

#Generate random initialization for parameters

param_len = (numGames * numFeatures) + (numUsers * numFeatures)
params0 = np.random.random(param_len) / 10

#Replace nan values

Y = np.nan_to_num(train.values)
R = np.where(np.isnan(train.values), 0, 1)


#Minimize cost function using gradient descent
    
alpha = 0.0001
max_iters = 15000
lam = 1

solution = gradDescent.minimize(costFunc.cost, costFunc.gradient, \
                             params0, Y, R, numUsers, numGames, \
                             numFeatures, lam, alpha, max_iters)
save_solution = pd.DataFrame(solution)
save_solution.to_csv(path+'Output/solution.csv')
print 'Solution saved'

solution_import = pd.read_csv(path+'Output/solution.csv', sep = ',', index_col = 0)
solution = solution_import.values

X = np.reshape(solution[0:numGames*numFeatures], [numGames, numFeatures])
Theta = np.reshape(solution[numGames*numFeatures:len(solution)], \
                            [numUsers, numFeatures])
combined = np.dot(X,Theta.T)
#normal = pd.DataFrame(value for value in normal)
#normalized = np.add(combined,normal)
ests = pd.DataFrame(combined, index = uniqueGames, columns = uniqueUsers)
ests.to_csv(path+'Output/estimates.csv')
print ests.head(5)






