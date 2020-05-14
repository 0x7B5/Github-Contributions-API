#!/usr/bin/env python3
import grequests
import requests

from flask import Flask, jsonify
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

app = Flask(__name__, static_url_path="")
app.config["TEMPLATES_AUTO_RELOAD"] = True
currentYear = datetime.today().year
baseurl = "https://github.com/"


@app.route('/contributions/<username>/<userCreationYear>', defaults={'todaysDate': None}, methods=['GET'])
@app.route('/contributions/<username>/<userCreationYear>/<todaysDate>', methods=['GET'])
def getAllCommits(username, userCreationYear, todaysDate):
    contributions = []
    years = []

    if todaysDate == None:
        print("NONE NONE")
        todaysDate = datetime.today()
    else:
        if isValidDate(todaysDate) != True:
            return jsonify({'Error': "Date couldn't be parsed"})
        todaysDate = datetime.strptime(todaysDate, '%Y-%m-%d')

    if isValidYear(userCreationYear) != True:
        return jsonify({'Error': "Creation year couldn't be parsed"})

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
            if (tempDate <= todaysDate):
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
        if (year != currentYear):
            otherUrl = "?tab=overview&from={}-01-01&to={}-12-31".format(
                year, year)
            urls.append(baseurl + "/" + username + otherUrl)
        else:
            urls.append(baseurl + "/" + username)

    return urls


def isValidYear(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def isValidDate(s):
    try:
        datetime.strptime(s, '%Y-%m-%d').date()
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def getWeekDay(dateToAnalyze):
    curDate = datetime.strptime(dateToAnalyze, '%Y-%m-%d').date()
    return (curDate.weekday()+1) % 7


@app.errorhandler(404)
def invalid_route(e):
    return jsonify({'Error': "Invalid Route"})


@app.route('/weeklyCount/<username>', defaults={'todaysDate': None}, methods=['GET'])
@app.route('/weeklyCount/<username>/<todaysDate>', methods=['GET'])
def getWeeklyCommits(username, todaysDate):
    if todaysDate == None:
        print("NONE NONE")
        todaysDate = datetime.today()
    else:
        if isValidDate(todaysDate) != True:
            return jsonify({'Error': "Date couldn't be parsed"})
        todaysDate = datetime.strptime(todaysDate, '%Y-%m-%d')

    weekAgoDate = (todaysDate - timedelta(days=7))

    page = requests.get(baseurl + username)

    soup = BeautifulSoup(page.content, 'html.parser')
    day_elems = soup.find_all('rect')
    contributions = []

    if day_elems == []:
        return jsonify({'Error': "Data Not Found"})

    for day_elem in day_elems:
        tempDate = datetime.strptime(
            day_elem.attrs['data-date'], '%Y-%m-%d')

        if (tempDate >= weekAgoDate and tempDate <= todaysDate):
            print(tempDate)
            contributions.append({
                'date': day_elem.attrs['data-date'],
                'color': day_elem.attrs['fill'],
                'count': int(day_elem.attrs['data-count']),
                'dayOfWeek': getWeekDay(day_elem.attrs['data-date'])
            })

    weeklyArray = [None] * 6
    for value in reversed(contributions):
        weeklyArray.insert(value["dayOfWeek"], value)
        if(value["dayOfWeek"] == 0):
            break

    # Really don't know why nulls are still in list so we have to do this hacky shit
    return jsonify({'today': [i for i in weeklyArray if i]})


@app.route('/monthlyCount/<username>', defaults={'todaysDate': None}, methods=['GET'])
@app.route('/monthlyCount/<username>/<todaysDate>', methods=['GET'])
def getMontlyCommits(username, todaysDate):
    if todaysDate == None:
        print("NONE NONE")
        todaysDate = datetime.today()
    else:
        if isValidDate(todaysDate) != True:
            return jsonify({'Error': "Date couldn't be parsed"})
        todaysDate = datetime.strptime(todaysDate, '%Y-%m-%d')

    monthAgoDate = (todaysDate - timedelta(days=30))
    print(type(monthAgoDate))
    page = requests.get(baseurl + username)

    soup = BeautifulSoup(page.content, 'html.parser')
    day_elems = soup.find_all('rect')
    contributions = []

    if day_elems == []:
        return jsonify({'Error': "Data Not Found"})

    for day_elem in day_elems:
        tempDate = datetime.strptime(
            day_elem.attrs['data-date'], '%Y-%m-%d')

        print(tempDate)
        if (tempDate >= monthAgoDate and tempDate <= todaysDate):
            contributions.append({
                'date': day_elem.attrs['data-date'],
                'color': day_elem.attrs['fill'],
                'count': int(day_elem.attrs['data-count']),
                'dayOfWeek': getWeekDay(day_elem.attrs['data-date'])
            })

    return jsonify({'today': contributions})


@app.route('/dayCount/<username>', defaults={'todaysDate': str(datetime.today().date())}, methods=['GET'])
@app.route('/dayCount/<username>/<todaysDate>', methods=['GET'])
def getDailyCommit(username, todaysDate):
    otherUrl = "?tab=overview&from={}-01-01&to={}-12-31".format(
        currentYear, currentYear)
    page = requests.get(baseurl + username + otherUrl)

    if isValidDate(todaysDate) != True:
        return jsonify({'Error': "Date couldn't be parsed"})

    soup = BeautifulSoup(page.content, 'html.parser')
    day_elems = soup.find_all('rect')
    contributions = []

    if day_elems == []:
        return jsonify({'Error': "Data Not Found"})

    for day_elem in day_elems:
        tempDate = datetime.strptime(
            day_elem.attrs['data-date'], '%Y-%m-%d').date()

        if (tempDate == datetime.strptime(todaysDate, '%Y-%m-%d').date()):
            contributions.clear()
            contributions.append({
                'date': day_elem.attrs['data-date'],
                'color': day_elem.attrs['fill'],
                'count': int(day_elem.attrs['data-count']),
                'dayOfWeek': getWeekDay(day_elem.attrs['data-date'])
            })

    return jsonify({'today': contributions})


@app.route('/aw/<username>/<userCreationYear>/<todaysDate>', methods=['GET'])
def getAppleWatchInfo(username, userCreationYear, todaysDate):
    contributions = []
    years = []
    if isValidDate(todaysDate) != True:
        return jsonify({'Error': "Date couldn't be parsed"})

    if isValidYear(userCreationYear) != True:
        return jsonify({'Error': "Creation year couldn't be parsed"})

    for i in range(int(userCreationYear), currentYear+1, 1):
        years.append(i)

    urls = fillUrls(username, years)
    results = grequests.map((grequests.get(u) for u in urls), size=len(years))
    todayCount = 0
    yesterdayCount = 0

    todaysDate = datetime.strptime(todaysDate, '%Y-%m-%d').date()

    for i in results:
        soup = BeautifulSoup(i.content, 'html.parser')
        day_elems = soup.find_all('rect')
        if day_elems == []:
            return jsonify({'Error': "Data Not Found"})

        for day_elem in day_elems:
            tempDate = datetime.strptime(
                day_elem.attrs['data-date'], '%Y-%m-%d').date()

            if (tempDate <= todaysDate):
                contributions.append({
                    'date': day_elem.attrs['data-date'],
                    'count': int(day_elem.attrs['data-count']),
                })

                if (tempDate == todaysDate):
                    print("Woah")
                    todayCount = int(day_elem.attrs['data-count'])
                    yesterdayCount = contributions[-2]['count']
            else:
                break
    currentStreak = calculateStreak(contributions, todaysDate, todayCount)

    dataToReturn = {
        'username': username,
        'commitsToday': todayCount,
        'commitsYesterday': yesterdayCount,
        'currentStreak': currentStreak,
        'creationYear': userCreationYear
    }

    return jsonify({'data': dataToReturn})


def calculateStreak(contributions, todaysDate, todayCount):
    if todayCount == 0:
        todaysDate = todaysDate - timedelta(days=1)

    counter = 0
    countingYet = False

    for i in reversed(contributions):
        if countingYet:
            if i['count'] > 0:
                counter += 1
            else:
                break

        if i['date'] == str(todaysDate):
            countingYet = True
            if i['count'] > 0:
                counter += 1

    return counter


if __name__ == '__main__':
    app.run(debug=False)
