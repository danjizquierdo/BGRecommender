import itertools
import pandas as pd
import numpy as np

ratings = pd.DataFrame()

folder = 'C://python27/'
for i in range(1,50):
    path  = folder + 'users' + str(i) + '.csv'
    current = pd.read_csv(path)
    users = current['user'].unique()
    for user in users:
        curr_user = current.loc[current['user'] == user].dropna(subset = ['rating'])
        curr_ratings = dict(itertools.izip(curr_user['gameid'], curr_user['rating']))
        curr_ratings['user'] = user
        ratings = ratings.append(curr_ratings, ignore_index = True)
ratings.set_index('user', inplace = True)
ratings.to_csv(folder+'Input.csv',header=True,index=False,encoding='utf-8')
