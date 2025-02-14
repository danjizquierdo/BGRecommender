''' Takes raw ratings matrix as input and returns mean normalized version
    as well as vector of average game ratings '''

import pandas as pd

ratings = pd.read_csv('<path>')

def mean_normalize(df): #currently only works column-wise
    df_norm = pd.DataFrame(np.zeros(df.shape), index = df.index, columns = df.columns)
    means = []
    for gameid, ratings in df.iteritems():
        game_mean = ratings.mean()
        means.append(game_mean)
        df_norm[gameid] = ratings - game_mean
    game_means = pd.Series(means, index = df.columns)
    return df_norm, game_means

normal, avg_ratings = mean_normalize(ratings)

normal.to_csv('<path>')
avg_ratings.to_csv('<path>')
