#!/usr/bin/env python3
# http dangerous option scanner

import threading
import requests
from optparse import OptionParser
import IPy
import re
# threading、requests、optparse、IPy、re

lock = threading.Lock()
threads = []

# 交互显示
def mainPage():
    #print("""
    #e.g:
    #    python3 http_options_scan.py -u https://www.baidu.com
    #    python3 http_options_scan.py -u http://192.168.1.100
    #    python3 http_options_scan.py -u http://192.168.1.0/24
    #""")
    option = OptionParser()
    option.add_option('-u', '--url', default=False, help='-u [http(s)://domain/ip(/mask length)]')
    option.add_option('-v', '--view', default=False, action='store_true', help='show more message')
    options, args = option.parse_args()
    url = options.url
    global view
    view = options.view
    if url == False and view == False:
        option.print_help()
        exit()
    print("Please wait...")
    return url

# 获取 HTTP Header
def getHTTPHead(url):
    try:
        response = requests.options(url, timeout = 3)
        # response.raise_for_status()
        if response.status_code == 200:
            return response.headers
        elif response.status_code == 501:
            response = requests.head(url, timeout = 3)
            response.raise_for_status()
            return response.headers
    except:
        return "HTTPError!"

# 检查 HTTP options 中是否有危险方法
def dangerOptions(head):
    try:
        server = head['Server']
        options = head['Allow']
        if (options.find("PUT") != -1 or options.find("MOVE") != -1):
            return (server, "HTTP Method Dangerous!")
        else:
            return (server, "HTTP Method Safe.")
    except:
        return (server, "HTTP Method Safe.")

# URL 处理
def urlSplit(url):
    pat = r'(([0-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])'
    is_ip = re.search(pat, url)
    urls = []
    if is_ip:
        ips = IPy.IP(url.split("://")[1])
        scheme = url.split("://")[0] + "://"
        for ip in ips:
            urls.append(scheme + str(ip))
    else:
        urls.append(url)
    return urls

# 输出扫描结果
def oneScan(url):
    lock.acquire()
    head = getHTTPHead(url)
    lock.release()
    if head == "HTTPError!":
        if view == True :
            print("{:<30} {}".format("[-] " + url, "Dead Target/HTTP Error!"))
        else:
            pass
    else:
        status = dangerOptions(head)
        print("\033[32m{:<30} {:<40} {}\033[0m".format("[+] " + url, status[0], status[1]))


def main():
    url = mainPage()
    urls = urlSplit(url)
    for url in urls:
        t = threading.Thread(target = oneScan, args = (url,))                   # 多线程调用 oneScan() 扫描
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Down.")


if __name__ == "__main__":
    main()
