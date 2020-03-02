#!/usr/bin/env python3
import requests
import json

r = requests.get('https://glass-watch-269518.appspot.com/todayCount/vlad-munteanu')
myJsonDict = r.json()['today']
commits = myJsonDict[0]['count']
date = myJsonDict[0]['date']

print("Date:", date)
print("Commits:", myJsonDict[0]['count'])

if commits == 0:
    print("")
    print("Go code.")
    


