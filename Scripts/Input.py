import pandas as pd
import numpy as np

games = pd.read_csv('C://Python27//gameslist.csv')
users = pd.read_csv('C://Python27//sample_userlist.csv')

game_set = set(games.values)
user_set = set(users.values)

ratings = pd.DataFrame(np.nan, index = users.values, columns = games.values)

for i in range(1,50):
    path  = 'C://python27/users' + str(i) + '.csv'
    current = pd.read_csv(path)
    for i, row in current.iterrows():
        if row['user'] in user_set and row['gameid'] in game_set:
            ratings.loc[ratings.index == row['user'], ratings.columns == row['gameid']] = row['rating']

ratings.to_csv('C://python27/Input.csv',header=True,index=False,encoding='utf-8')
