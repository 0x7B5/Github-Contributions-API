#!/usr/bin/env python3
import requests

from flask import Flask, jsonify
from datetime import datetime
from bs4 import BeautifulSoup



app = Flask(__name__, static_url_path="")
currentYear = datetime.today().year
baseurl = "https://github.com/"
otherUrl = "?tab=overview&from={}-01-01&to={}-12-31".format(currentYear,currentYear)

@app.route('/contributions/<username>', methods=['GET'])
def getAllCommits(username):
    print(isValidUser(username))
    
    if isValidUser(username) == False:
        return jsonify("User does not exist")
    getUserCreationYear(username)
    page = requests.get(baseurl + username + otherUrl)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    day_elems = soup.find_all('rect')
    
    contributions = [ ]
    
    for day_elem in day_elems:
        tempDate = datetime.strptime(day_elem.attrs['data-date'], '%Y-%m-%d')
        if (tempDate <= datetime.today()):
            contributions.append({
                                    'Date': day_elem.attrs['data-date'],
                                    'Fill': day_elem.attrs['fill'],
                                    'Contributions': day_elem.attrs['data-count']
                                 })
        else:
            break
    return jsonify({'Data': contributions})
  
  
@app.route('/DailyContributions/<username>', methods=['GET'])
def getDailyCommit():
    return 1

def getUserCreationYear(username):
    r = requests.get("https://api.github.com/users/{}".format(username))
    data = r.json()
    return data['created_at'].split("-")[0]
    
def isValidUser(username):
    r = requests.get("https://api.github.com/users/{}".format(username))
    data = r.json()
    
    if data['message'] == "Not Found":
        return False
    return True
    
if __name__ == '__main__':
    app.run(debug=True)


