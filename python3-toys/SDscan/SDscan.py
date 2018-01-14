#!/usr/bin/env python3
# sub-domain scan tool

import requests
import re
import socket

# TODO(Aquilao@outlook.com): Set usage options.
# TODO(Aquilao@outlook.com): Fix out the script find wrong sub-domains in baidu.

# user interface
def mainPage():
	print(" ____  ____                       ")
	print("/ ___||  _ \ ___  __ _  ___ _ __  ")
	print("\___ \| | | / __|/ _` |/ __| '_ \ ")
	print(" ___) | |_| \__ \ (_| | (__| | | |")
	print("|____/|____/|___/\__,_|\___|_| |_|")
	print("---------------------------------------------")
	print("* Version  1.0")
	print("* GitHub   https://github.com/Aquilao/Toy-Box")
	print("---------------------------------------------")
	domain = input('Please input domain:')
	print('Please wait...')
	print("")
	return domain

# get sub-domains from one page
def GetonePage(domain, page):
	try:
		response = requests.get('http://www.baidu.com/s?wd=site:' + domain + '&pn=' + str(page)) 
		response.raise_for_status()
		subdomains = re.findall(r'style="text-decoration:none;">(.*?)/', response.text)
		return subdomains
	except:
		return 'Error!'

# sub-domain analyze ip address
def Getip(subdomain):
	try:
		ip = socket.gethostbyname(subdomain)
		return ip
	except:
		return "Ip analysis failed!"

def main():
	site = []
	domain = mainPage()
	for page in range(100):		# scan sub-mains in 100 pages
		page = page * 10
		subdomains = GetonePage(domain, page)
		site += list(subdomains)
		site = list(set(site))		# Discard duplicate sub-domains
	subdomain_num = 0
	for i in range(len(site)):
		i += 1
		subdomain = site[i - 1]
		if len(subdomain) > 6:
			ip = Getip(subdomain)
			subdomain_num += 1
		else:
			pass
		print('%-5d%-40s%-40s' % (subdomain_num, subdomain, ip))
if __name__ == '__main__':
	main()