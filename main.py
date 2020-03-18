#!/usr/bin/env python3
import grequests
import requests

from flask import Flask, jsonify
from datetime import datetime
from bs4 import BeautifulSoup

app = Flask(__name__, static_url_path="")
currentYear = datetime.today().year
baseurl = "https://github.com/"


@app.route('/contributions/<username>/<userCreationYear>', methods=['GET'])
def getAllCommits(username, userCreationYear):
    contributions = []
    years = []

    if isValidYear(userCreationYear) != True:
        return jsonify({'Error': "Data Not Found"})

    for i in range(int(userCreationYear), currentYear+1, 1):
        years.append(i)

    urls = fillUrls(username, years)
    results = grequests.map((grequests.get(u) for u in urls), size=len(years))

    for i in results:
        soup = BeautifulSoup(i.content, 'html.parser')
        day_elems = soup.find_all('rect')
        if day_elems == []:
            return jsonify({'Error': "Data Not Found"})

        for day_elem in day_elems:
            tempDate = datetime.strptime(
                day_elem.attrs['data-date'], '%Y-%m-%d')
            if (tempDate <= datetime.today()):
                contributions.append({
                    'date': day_elem.attrs['data-date'],
                    'color': day_elem.attrs['fill'],
                    'count': int(day_elem.attrs['data-count']),
                    'dayOfWeek': getWeekDay(day_elem.attrs['data-date'])
                })
            else:
                break

    return jsonify({'contributions': contributions})


def fillUrls(username, yearsToGet):
    urls = []

    for year in yearsToGet:
        otherUrl = "?tab=overview&from={}-01-01&to={}-12-31".format(year, year)
        urls.append(baseurl + "/" + username + otherUrl)

    return urls


def isValidYear(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def getWeekDay(dateToAnalyze):
    curDate = datetime.strptime(dateToAnalyze, '%Y-%m-%d').date()
    return (curDate.weekday()+1) % 7


@app.errorhandler(404)
def invalid_route(e):
    return jsonify({'Error': "Invalid Route"})


@app.route('/todayCount/<username>', methods=['GET'])
def getDailyCommit(username):
    otherUrl = "?tab=overview&from={}-01-01&to={}-12-31".format(
        currentYear, currentYear)
    page = requests.get(baseurl + username + otherUrl)

    soup = BeautifulSoup(page.content, 'html.parser')
    day_elems = soup.find_all('rect')
    contributions = []

    if day_elems == []:
        return jsonify({'Error': "Data Not Found"})

    for day_elem in day_elems:
        tempDate = datetime.strptime(
            day_elem.attrs['data-date'], '%Y-%m-%d').date()
        todayDate = datetime.today().date()

        if (tempDate == todayDate):
            contributions.clear()
            contributions.append({
                'date': day_elem.attrs['data-date'],
                'color': day_elem.attrs['fill'],
                'count': int(day_elem.attrs['data-count']),
                'dayOfWeek': getWeekDay(day_elem.attrs['data-date'])
            })

    return jsonify({'today': contributions})


if __name__ == '__main__':
    app.run(debug=False)
