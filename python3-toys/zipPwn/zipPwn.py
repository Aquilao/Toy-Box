#!/usr/bin/env python3

# zipPwn -- zip password crack tool

import os
import zipfile
from optparse import OptionParser

# TODO(Aquilao@outlook.com): Add multithreading modules.
'''
-o output path
-t multithreading
'''

# User interface
def mainPage():
    option = OptionParser()
    option.add_option('-f', '--file', default=False, help='-f zip file path')
    option.add_option('-d', '--wordlist', default=False, help='-d wordlist path')
    options, args = option.parse_args()
    file_path = options.file
    dict_path = options.wordlist
    if file_path == False and dict_path == False:
        option.print_help()
        exit()
    return (file_path, dict_path)

# Read wordlist and transfer unzip()
def read_dict(zip_file, dict_path, path):
    pwd_file = open(dict_path)
    for line in pwd_file.readlines():
        passwd = line.strip('\n')
        flag = unzip(zip_file, passwd, path)
        if flag == 1:
            break
    if flag == 0:
        print('Sorry, maybe you should use other wordlist.')

# Extract the zip file
def unzip(zip_file, passwd, path):
    try:
        zip_file.extractall(path ,pwd = passwd.encode('utf-8'))
        print('Success! password is:' + passwd)
        return 1
    except:
        return 0

def main():
    file_path, dict_path = mainPage()
    zip_file = zipfile.ZipFile(file_path)
    path = os.path.split(file_path)[0]
    read_dict(zip_file, dict_path, path)

if __name__ == "__main__":
    main()
