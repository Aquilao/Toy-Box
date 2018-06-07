#!/usr/bin/env python3
# http option scanner

import threading
import requests
import sys
import IPy
import re

lock = threading.Lock()
threads = []

# 交互显示
def mainPage():
    url = input("Please input url [http(s)://domain/ip(/mask length)]:")
    return url

# 获取 HTTP Header
def getHTTPHead(url):
    try:
        response = requests.options(url, timeout = 3)
        response.raise_for_status()
        return response.headers
    except:
        return "HTTPError!"

# 检查 HTTP options 中是否有危险方法
def dangerOptions(head):
    try:
        options = head['Allow']
        if (options.find("PUT") != -1 or options.find("MOVE") != -1):
            return "HTTP Method Dangerous!"
        else:
            return "HTTP Method Safe."
    except:
        return "HTTP Method Safe."

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
    url
    head = getHTTPHead(url)
    lock.release()
    if head == "HTTPError!":
        print("{} {:<25} {}".format("[-]", url, "Dead Target/HTTP Error!"))
    else:
        status = dangerOptions(head)
        print("\033[32m{} {:<25} {}\033[0m".format("[+]", url, status))


def main():
    url = mainPage()
    urls = urlSplit(url)
    for url in urls:
        t = threading.Thread(target = oneScan, args = (url,))                   # 多线程调用 oneScan() 扫描
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
