#!/usr/bin/env python3

# RFC search -- RFC document search tool

import os
import requests
from bs4 import BeautifulSoup

# User interface
def mainPage():
    info = """
     ____  _____ ____                           _
    |  _ \|  ___/ ___|  ___  ___  __ _ _ __ ___| |__
    | |_) | |_ | |     / __|/ _ \/ _` | '__/ __| '_ \\
    |  _ <|  _|| |___  \__ \  __/ (_| | | | (__| | | |
    |_| \_\_|   \____| |___/\___|\__,_|_|  \___|_| |_|
    --------------------------------------------------
    * Version 1.0
    * GitHub   https://github.com/Aquilao/Toy-Box
    --------------------------------------------------
    """

    print(info)
    id = input('Please input RFC id:')
    print("Please waiting a moment...")
    return id


# Get the html text
def getHTMLText(rfcid):
    url = 'https://tools.ietf.org/html/rfc'
    try:
        r = requests.get(url + rfcid)
        r.raise_for_status()
        return r.text
    except:
        return 'HTTP Error!'

# Analysis the html text
def mksoup(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.title.string)
    [s.extract() for s in soup('head')]    #Remove head tag and the text between them
    return soup

# Save RFC document
def saveRFC(soup, rfcid):
    path = os.path.expandvars('$HOME') + '/Downloads/'
    file_path = path + 'rfc' + rfcid + '.txt'
    text = soup.get_text()    # Remove all of the tags
    f = open(file_path, 'w+')
    f.write(text)
    f.close()
    print('Success! download in ' + path)

def main():
    rfcid = mainPage()
    html = getHTMLText(rfcid)
    soup = mksoup(html)
    saveRFC(soup, rfcid)

if __name__ == '__main__':
    main()
