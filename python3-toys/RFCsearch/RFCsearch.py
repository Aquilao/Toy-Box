#!/usr/bin/env python3
#RFC search tool

import os
import requests as rq
from bs4 import BeautifulSoup as bs

def mainPage():
    print(" ____  _____ ____                           _     ")
    print("|  _ \|  ___/ ___|  ___  ___  __ _ _ __ ___| |__  ")
    print("| |_) | |_ | |     / __|/ _ \/ _` | '__/ __| '_ \\")
    print("|  _ <|  _|| |___  \__ \  __/ (_| | | | (__| | | |")
    print("|_| \_\_|   \____| |___/\___|\__,_|_|  \___|_| |_|")
    print("--------------------------------------------------")
    print("* Version 1.0")
    print("* GitHub   https://github.com/Aquilao/Toy-Box")
    print("--------------------------------------------------")
    id = input('Please input RFC id:')
    return id

def getHTMLText(rfcid):
    url = 'https://tools.ietf.org/html/rfc'
    try:
        r = rq.get(url + rfcid)
        r.raise_for_status()
        return r.text
    except:
        return 'HTTP Error!'

def mksoup(html):
    soup = bs(html, "html.parser")
    print(soup.title.string)
    [s.extract() for s in soup('head')]
    return soup

def saveRFC(soup, rfcid):
    path = os.path.expandvars('$HOME') + '/Downloads/'
    file_path = path + 'rfc' + rfcid + '.txt' 
    text = soup.get_text()
    f = open(file_path, 'w+')
    f.write(text)
    f.close()
    print('Success!save in ' + path)

def main():
    rfcid = mainPage()
    html = getHTMLText(rfcid)
    soup = mksoup(html)
    saveRFC(soup, rfcid)

if __name__ == "__main__":
    main()
