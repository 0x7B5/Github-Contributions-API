#!/usr/bin/env python3
import requests
import sys


from datetime import datetime
from bs4 import BeautifulSoup


currentYear = datetime.today().year
baseurl = "https://github.com/"


def isValidUser(username):
## There's an API limit that I'm hitting for some reason
## SO essentially, we need to manually parse the github site to see if they are
## a valid user or not because the api is being weird
    print("hey")
    page = requests.get("https://github.com/".format(username))
    soup = BeautifulSoup(page.content, 'html.parser')

    myBigDiv = soup.find_all(class_="p-name")
    

    
    print(myBigDiv)
    
    File_object = open(r"yuhhh.html","w")
    File_object.write(str(page.content))
    

#    print(myBigDiv)
    yuhList = []
    
#    for i in divTag:
#        print(i)
#        print("")
#
#    for tag in divTag:
#        tdTags = tag.find_all("a", {"class": "js-year-link filter-item px-3 mb-2 py-2 "})
#        for tag in tdTags:
#            print(tag.text)
#            yuhList.append(tag.text)
#
    returnVal = page.text
    return "idk"


if __name__ == "__main__":
    print("hey")
    print(str(sys.argv))
    myList = str(sys.argv)
    
    isValidUser(myList[1])
    
