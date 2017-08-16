''' Create training sample with ratings for all games
    with > 10 ratings '''

games = {}

for i in range(1,50):
    path  = 'C://Python27/users' + str(i) + '.csv'
    current = pd.read_csv(path).dropna(subset = ['rating'])
    for i, row in current.iterrows():
        if row['gameid'] not in games.keys():
            games[row['gameid']] = [row['user']]
        else:
            games[row['gameid']].append(row['user'])

games_subset = {k: v for k, v in games.iteritems() if len(v) > 9}

