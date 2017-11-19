#!/usr/bin/env python3
#zip crack tool

import os
import zipfile

def mainPage():
    print("     _       ____                 ")
    print(" ___(_)_ __ |  _ \__      ___ __  ")
    print("|_  / | '_ \| |_) \ \ /\ / / '_ \ ")
    print(" / /| | |_) |  __/ \ V  V /| | | |")
    print("/___|_| .__/|_|     \_/\_/ |_| |_|")
    print("      |_|                         ")
    print("---------------------------------------------")
    print("* Version 1.0")
    print("* GitHub   https://github.com/Aquilao/Toy-Box")
    print("---------------------------------------------")
    file_path = input('Please input zip file path:')
    return file_path

def read_dict(zip_file, path):
    dict_path = input('Please input dict path:')
    pwd_file = open(dict_path)
    for line in pwd_file.readlines():
        passwd = line.strip('\n')
        flag = unzip(zip_file, passwd, path)
        if flag == 1:
            break
    if flag == 0:
        print('Sorry, maybe you should use other dict')

def unzip(zip_file, passwd, path):
    try:
        zip_file.extractall(path ,pwd = passwd.encode('utf-8'))
        print('Success! password is:' + passwd)
        return 1
    except:
        return 0

def main():
    file_path = mainPage()
    zip_file = zipfile.ZipFile(file_path)
    path = os.path.split(file_path)
    path = path[0]
    read_dict(zip_file, path)

if __name__ == "__main__":
    main()
