from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

output=[]
for num in range(1,456):
    req = requests.get('https://www.boardgamegeek.com/browse/user/numreviews/page/'+str(num))
    site = req.content
    soup = BeautifulSoup(site,"lxml")
    for link in soup.find_all('div',{'class':'avatarblock'}):
       output.append((link.get('data-username')) + ',')
    time.sleep(5)
with open('C:\\python27\users.txt','a') as f:
    for line in output:
       f.write(line.encode('utf8'))
with open('users.txt','r') as f:
    data=f.read()
    data=data.split(',')
    stuff=pd.Series(data)
    series=pd.Series(stuff.unique())
    series.to_csv('uniqueusers.csv')
