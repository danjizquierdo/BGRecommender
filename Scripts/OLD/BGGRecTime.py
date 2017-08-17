
# coding: utf-8

# In[6]:

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
        newrow['gameid'] = str(item.attrib['objectid'])
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
''' Save unique users under userlist instead of what I have here'''
userlist = []
with open("C://python27/timeusers.csv",'r') as csvfile:
    readCSV = csv.reader(csvfile,delimiter=',')
    for row in readCSV:
        userlist.append(row[1])
for username in userlist:
    start_time=time.time()
    userdata = get_user(username)
    if not userdata.empty:
        all_data = all_data.append(userdata)
    gap=time.time()-start_time
    if gap<5:
        time.sleep(5-gap)
print all_data.head()
''' Change directory or whatever you might need to save data in the right place '''
all_data.to_csv('C://python27/timetest.csv',header=True,index=False,encoding='utf-8')

