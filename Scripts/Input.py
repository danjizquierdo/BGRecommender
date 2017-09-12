import pandas as pd
import numpy as np

#Function that creates a list of games ready for input
def input_games(path='C:/Python27/BGRec/GameDB/gameslist.csv'):
    games = pd.read_csv(path, index_col=0)
    game_set = set()
    for item in games.values.tolist():
        game_set.update(item)
    return game_set

#Function that creates a list of users ready for input
def input_users(path='C:/Python27/BGRec/UserDB/sample_users.csv'):
    users = pd.read_csv(path, index_col=0)
    user_set = set()
    for item in users.values.tolist():
        user_set.update(item)
    return user_set

def create_ratings(ratings,df):
    for i, row in df.iterrows():
        if row['user'] in user_set and row['gameid'] in game_set:
            ratings.loc[ratings.index == row['user'], ratings.columns == row['gameid']] = row['rating']
    return ratings

#When run creates a rating matrix with values of nan for non-rated games, and ratings for rated games
if __name__ == "__main__":
    import sys
    game_set=input_games()
    user_set=input_users()
    ratings = pd.DataFrame(np.nan, index = user_set, columns = game_set)

    for i in range(1,50):
        path  = 'C://python27/BGRec/UserDB/users' + str(i) + '.csv'
        current = pd.read_csv(path)
        ratings=create_ratings(ratings,current)
     
#First argument boolean to create Input file or not
    if sys.argv[1]==True:
        ratings.to_csv('C://python27/BGRec/Raw/Input.csv',header=True,index=True,encoding='utf-8')
    else:
        print 'Processing complete.'
