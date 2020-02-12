#!/usr/bin/env python3
import requests
from datetime import datetime
from bs4 import BeautifulSoup

baseurl = "https://github.com/vlad-munteanu?tab=overview&from=2020-01-01&to=2020-12-31"
username = "vlad-munteanu"

page = requests.get(baseurl)
#print(page.content)
soup = BeautifulSoup(page.content, 'html.parser')

day_elems = soup.find_all('rect')

for day_elem in day_elems:
    tempDate = datetime.strptime(day_elem.attrs['data-date'], '%Y-%m-%d')
    if (tempDate <= datetime.today()):
        print("Date:", day_elem.attrs['data-date'], "Fill:", day_elem.attrs['fill'], "Contributions:", day_elem.attrs['data-count'])
    else:
        break

currentYear = datetime.now().year 
print(currentYear)
