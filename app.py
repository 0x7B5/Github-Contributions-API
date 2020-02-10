#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

baseurl = "https://github.com/vlad-munteanu?tab=overview&from=2020-01-01&to=2020-12-31"
username = "vlad-munteanu"

page = requests.get(baseurl)
print(type(page))
#print(page.content)
soup = BeautifulSoup(page.content, 'html.parser')

day_elems = soup.find_all(class_='day')

for day_elem in day_elems:
    print(day_elem, end='\n')
