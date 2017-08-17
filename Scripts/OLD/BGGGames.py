
# coding: utf-8

# In[1]:

import requests
from xml.etree import ElementTree as ET
import pandas as pd
import numpy as np
import time
import csv

# In[2]:

def get_game(gameid):
    newrow = {}
    url = 'https://www.boardgamegeek.com/xmlapi/boardgame/' + str(gameid) + '?stats=1'
    r = requests.get(url)
    try:
        game = ET.fromstring(r.content)
    except:
        print 'Game ' + gameid + ' could not be parsed'
        return newrow
    for item in game[0]:
        if item.tag in ['boardgameversion','boardgamepodcastepisode','poll','thumbnail','image']:
            continue
        elif item.tag == 'statistics':
            for stat in item[0]:
                if stat.tag in ['usersrated','average','bayesaverage']:
                    newrow[stat.tag] = stat.text
        elif item.tag not in newrow.keys():
            newrow[item.tag] = [item.text]
        else:
            newrow[item.tag].append(item.text)
    for var in newrow.keys():
        if len(newrow[var]) == 1:
            newrow[var] = newrow[var][0]
    return newrow

       
all_games = pd.DataFrame()
game_list= pd.Series()

for i in range(1,50):
    df=pd.read_csv("C://python27/users"+str(i)+".csv")
    game_list=game_list.append(df.gameid, ignore_index=True) 
uniquegames = game_list.unique()
for gameid in uniquegames:
    last_call = time.time()
    gamedata = get_game(gameid)
    if gamedata:
        all_games = all_games.append(gamedata, ignore_index = True)
    gap = time.time() - last_call
    if gap < 5:
        time.sleep(5.1 - gap)
    
all_games.to_csv('C://python27/games.csv',header=True,index=False,encoding='utf-8')


# In[3]:

def nanchecker(value):
    try:
        out = np.isnan(value)
    except TypeError:
        out = False
    return out

def expand_category(df,variable):
    rowlist = df[variable].tolist()
    temp = df[variable].dropna().tolist()
    temp2 = pd.Series([item for row in temp for item in row])
    categories = temp2.unique()
    dummies = pd.DataFrame()
    for row in rowlist:
        rowdata = {}
        if nanchecker(row):
            for category in categories:
                rowdata[category] = 0
        else:
            for category in categories:
                if category in row:
                    rowdata[category] = 1
                else:
                    rowdata[category] = 0
        dummies = dummies.append(rowdata, ignore_index = True)
    return dummies

