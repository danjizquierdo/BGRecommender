from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import numpy as np
import csv
from xml.etree import ElementTree as ET

#Finds all users who have submitted reviews on BGG, saved to a csv file
def find_users(end=456, path='C://python27/'):
    output=[]
    for num in range(1,end):
        req = requests.get('https://www.boardgamegeek.com/browse/user/numreviews/page/'+str(num))
        site = req.content
        soup = BeautifulSoup(site,"lxml")
        for link in soup.find_all('div',{'class':'avatarblock'}):
           output.append((link.get('data-username')) + ',')
        time.sleep(5)
    with open(path+'users.txt','a') as f:
        for line in output:
           f.write(line.encode('utf8'))
    with open('users.txt','r') as f:
        data=f.read()
        data=data.split(',')
        stuff=pd.Series(data)
        series=pd.Series(stuff.unique())
        series.to_csv('uniqueusers.csv')
    return len(output)

#Scrapes user information through BGG's XML API
def get_user(username):
    userstats = pd.DataFrame()
    url = 'https://www.boardgamegeek.com/xmlapi/collection/' + username 
    r = requests.get(url)
    try:
        collection = ET.fromstring(r.content)
    except xml.etree.ElementTree.ParseError:
        print 'User ' + username + ' could not be parsed'
        return userstats
    for item in collection:
        newrow = {}
        try:
            newrow['gameid'] = str(item.attrib['objectid'])
        except:
            print 'Game ' + username + ' could not be IDed'
            continue
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

#Reads a csv file containing unique usernames and returns that list
def import_users(path='C:/python27/uniqueusers.csv'):
    userlist=[]
    with open(path,'r') as csvfile:
        readCSV = csv.reader(csvfile,delimiter=',')
    for row in readCSV:
        userlist.append(row[1])
    return userlist

#Runs through a list of usernames and retrieves their information from BGG
#Returns the number of files that have been created
def scrape_users(userlist, counter=1):
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
    return str(counter)+ ' files created.'

#Scrapes game information through BGG's XML API
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

#Runs through a list of games and retrieves their information from BGG
#Returns the number of files that have been created
def find_games(uniquegames,game_counter=1,path='C://python27/'):
    for gameid in uniquegames:
        last_call = time.time()
        gamedata = get_game(gameid)
        if gamedata:
            all_games = all_games.append(gamedata, ignore_index = True)
        if all_games.shape[0] > 50000:
            all_games.to_csv(path+'games' + str(game_counter) + '.csv',header=True,index=False,encoding='utf-8')
            all_games = pd.DataFrame()
            game_counter += 1
        gap = time.time() - last_call
        if gap < 5:
            time.sleep(5.1 - gap)
    return str(game_counter) + ' files created.'

#If run as a script, finds a list of users from BGG, scrapes their information
#and scrapes the information for all the games that the users have collectively
#rated
if __name__ == "__main__":
    import sys
    find_users()
    all_data = pd.DataFrame()
    game_list = pd.Series()
    counter = 1
    userlist = import_users()
    scrape_users(userlist)
    all_games = pd.DataFrame()
    uniquegames = game_list.unique()
    find_games(uniquegames)
    
