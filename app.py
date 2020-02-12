#!/usr/bin/env python3
import requests
from flask import Flask, jsonify
from datetime import datetime
from bs4 import BeautifulSoup


app = Flask(__name__, static_url_path="")

@app.route('/contributions/<username>', methods=['GET'])
def getAllCommits(username):
#    username = request.args.get('username')
    baseurl = "https://github.com/"
    otherUrl = "?tab=overview&from={}-01-01&to={}-12-31".format(datetime.today().year,datetime.today().year)
    
    
    page = requests.get(baseurl + username + otherUrl)
    #print(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    day_elems = soup.find_all('rect')
    
    contributions = [ ]
    
    for day_elem in day_elems:
        tempDate = datetime.strptime(day_elem.attrs['data-date'], '%Y-%m-%d')
        if (tempDate <= datetime.today()):
#            print("Date:", day_elem.attrs['data-date'], "Fill:", day_elem.attrs['fill'], "Contributions:", day_elem.attrs['data-count'])
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

if __name__ == '__main__':
    app.run(debug=True)


