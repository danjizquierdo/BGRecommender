''' Create training sample with ratings for all games
    with > 10 ratings '''
import pandas as pd
import random
random.seed(42)

games = {}

for i in range(1,50):
    path  = 'C://Python27/BGRec/UserDB/users' + str(i) + '.csv'
    current = pd.read_csv(path).dropna(subset = ['rating'])
    for i, row in current.iterrows():
        if row['gameid'] not in games.keys():
            games[row['gameid']] = set([row['user']])
        else:
            games[row['gameid']].add(row['user'])

games_subset = {k: v for k, v in games.iteritems() if len(v) > 24}

gameslist = pd.Series(games_subset.keys())
gameslist.to_csv('C://Python27/BGRec/GameDB/gameslist.csv')

sample_users = set()

for user_list in games_subset.values():
    n = len(user_list)
    new_users = user_list.difference(sample_users)
    new_n = len(new_users)
    while len(new_users) > .4 * n:
        samp = random.choice(tuple(new_users))
        sample_users.add(samp)
        new_users.remove(samp)

sample_userlist = pd.Series(list(sample_users))
sample_userlist.to_csv('C://Python27/BGRec/UserDB/sample_users.csv')
