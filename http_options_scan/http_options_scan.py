#!/usr/bin/env python3
# http dangerous option scanner
# by Aquilao

import threading
import requests
from optparse import OptionParser
from concurrent.futures import ThreadPoolExecutor
import IPy
import re
import math
import sys


#lock = threading.Lock()

# 交互显示
def mainPage():
    #print("""
    #e.g:
    #    python3 http_options_scan.py -u https://www.baidu.com
    #    python3 http_options_scan.py -u http://192.168.1.100
    #    python3 http_options_scan.py -u http://192.168.1.0/24
    #""")
    banner = """
     _     _   _                       _   _                                       
    | |__ | |_| |_ _ __     ___  _ __ | |_(_) ___  _ __  ___   ___  ___ __ _ _ __  
    | '_ \| __| __| '_ \   / _ \| '_ \| __| |/ _ \| '_ \/ __| / __|/ __/ _` | '_ \ 
    | | | | |_| |_| |_) | | (_) | |_) | |_| | (_) | | | \__ \ \__ \ (_| (_| | | | |
    |_| |_|\__|\__| .__/   \___/| .__/ \__|_|\___/|_| |_|___/ |___/\___\__,_|_| |_|
                  |_|           |_|                                                
     """
    print(banner)
    option = OptionParser()
    option.add_option('-u', '--url', default=False, help='-u [http(s)://domain/ip(/mask length)]')
    option.add_option('-t', '--thread', default=256, help='-t <thread_number>, default 256')
    option.add_option('-v', '--view', default=False, action='store_true', help='show more message')
    option.add_option('-d', '--dangerous', default=False, action='store_true', help='only show dangerous message')
    options, args = option.parse_args()
    url = options.url
    global view, dangerous, thread
    view = options.view
    dangerous = options.dangerous
    thread = int(options.thread)
    if url == False:
        option.print_help()
        exit()
    return url

# 获取 HTTP Header
def getHTTPHead(url):
    requests.packages.urllib3.disable_warnings()                                # 忽略由于建立不安全的 https 连接导致 urllib3 库产生的警告
    try:
        response = requests.get(url, timeout = 3, verify=False)
        code = response.status_code
        if code == 200:
            try:
                response = requests.options(url, timeout = 3)
                response.raise_for_status()
            except:
                pass
        return response.headers
    except:
        return "HTTPError!"

# 检查 HTTP options 中是否有危险方法
def dangerOptions(head):
    try:
        server = ' '
        server = head['Server']
        options = head['Allow']
        if (options.find("PUT") != -1 or options.find("MOVE") != -1):
            return (server, 1)                                                  # 1 是 HTTP Method Dangerous!
        else:
            return (server, 0)                                                  # 0 是 HTTP Method Safe.
    except:
        return (server, 0)

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

# 进度条
def progress_bar(portion, total, info):
    part = total / 50
    count = math.ceil(portion / part)
    #sys.stdout.write('\r')
    sys.stdout.write(' ' * 60 + '\r')
    sys.stdout.flush()
    if info:
        print(info)
    sys.stdout.write(('[%-50s]%.2f%%' % (('>' * count), portion / total * 100))+'\r')
    sys.stdout.flush()
    if portion >= total:
        sys.stdout.write('\n')
        return True

# 输出扫描结果
def oneScan(url):
    #lock.acquire()
    head = getHTTPHead(url)
    #lock.release()
    info = ''
    if head == "HTTPError!" and view == True:
        info = "{:<30} {}".format("[-] " + url, "Dead Target/HTTP Error!")
    elif head == "HTTPError!" and view == False:
        pass
    else:
        status = dangerOptions(head)
        if status[1] == 0:
            if dangerous == False:
                info = "\033[32m{:<30} {:<40} {}\033[0m".format("[+] " + url, status[0], "HTTP Method Safe.")
            #print("\033[32m{:<30} {:<40} {}\033[0m".format("[+] " + url, status[0], "HTTP Method Safe."))
        else:
            info = "\033[31m{:<30} {:<40} {}\033[0m".format("[+] " + url, status[0], "HTTP Method Dangerous!")
            #print("\033[31m{:<30} {:<40} {}\033[0m".format("[+] " + url, status[0], "HTTP Method Dangerous!"))
    return info

def main():
    url = mainPage()
    urls = urlSplit(url)
    threads = []
    executor = ThreadPoolExecutor(max_workers=thread)
    portion = 0
    total = len(urls)
    print("\033[34m{} {} target {} {} threads\033[0m".format("[*]", str(total), "\n[*]", str(thread)))
    for info in executor.map(oneScan, urls):
        portion += 1
        sum = progress_bar(portion, total, info)
        if sum:
            break
    print("Done.")


if __name__ == "__main__":
    main()