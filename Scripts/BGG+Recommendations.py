# coding: utf-8
# In[59]:
import requests
from xml.etree import ElementTree as ET
import pandas as pd
import time
import csv

def get_user(username):
    userstats = pd.DataFrame()
    url = 'https://www.boardgamegeek.com/xmlapi/collection/' + username 
    r = requests.get(url)
    collection = ET.fromstring(r.content)
    for item in collection:
        newrow = {}
        newrow['gameid'] = item.attrib['objectid']
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
userlist = []
with open("C:\\python27\uniqueusers.csv",'r') as csvfile:
    readCSV = csv.reader(csvfile,delimiter=',')
    for row in readCSV:
        userlist.append(row[1])
for username in userlist:
    userdata = get_user(username)
    all_data = all_data.append(userdata)
    time.sleep(5)
all_data.to_csv('games.csv')
