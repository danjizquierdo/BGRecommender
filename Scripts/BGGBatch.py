
# coding: utf-8

# In[1]:

import requests
from xml.etree import ElementTree as ET
import pandas as pd
import numpy as np
import time
import csv

def get_user(username):
    userstats = pd.DataFrame()
    url = 'https://www.boardgamegeek.com/xmlapi/collection/' + username 
    r = requests.get(url)
    try:
        collection = ET.fromstring(r.content)
    except:
        print 'User ' + username + ' could not be parsed'
        return userstats
    for item in collection:
        newrow = {}
        try:
            newrow['gameid'] = str(item.attrib['objectid'])
        except:
            print 'User ' + username + ' could not be IDed'
            return userstats
        for feature in item:
            if feature.tag == 'stats':
                for stat in feature:
                    if stat.attrib['value'] != 'N/A':
                        newrow[stat.tag] = float(stat.attrib['value'])
            elif feature.tag == 'status':
                for name, stat in feature.attrib.iteritems():
                    if name != 'lastmodified': 
                        newrow[name] = int(stat)
            elif feature.tag in ['name','comment']:
                newrow[feature.tag] = feature.text
        userstats = userstats.append(newrow, ignore_index = True)
    userstats['user'] = username
    return userstats

all_data = pd.DataFrame()
game_list = pd.Series()
counter = 1

userlist = []
with open("C://python27/uniqueusers.csv",'r') as csvfile:
    readCSV = csv.reader(csvfile,delimiter=',')
    for row in readCSV:
        userlist.append(row[1])
for username in userlist:
    last_call = time.time()
    userdata = get_user(username)
    if not userdata.empty:
        all_data = all_data.append(userdata)
        game_list = game_list.append(userdata['gameid'])
    if all_data.shape[0] > 50000:
        all_data.to_csv('C://python27/users' + str(counter) + '.csv',header=True,index=False,encoding='utf-8')
        all_data = pd.DataFrame()
        counter += 1
    gap = time.time() - last_call
    if gap < 5:
        time.sleep(5.1 - gap)




# In[2]:

def get_game(gameid):
    newrow = {}
    url = 'https://www.boardgamegeek.com/xmlapi/boardgame/' + gameid + '?stats=1'
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

uniquegames = game_list.unique()
for gameid in uniquegames[0:9]:
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

