#!/usr/bin/env python3
# http dangerous option scanner
# by Aquilao

import threading
import requests
import socket
import struct
from optparse import OptionParser
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED # test
import IPy
import re
import cgitb                                                                    # test

# lock = threading.Lock()
threads = []
dic = {}

# 交互显示
def mainPage():
    #print("""
    #e.g.
    #    python3 http_options_scan.py -u https://www.baidu.com
    #    python3 http_options_scan.py -u http://192.168.1.1
    #    python3 http_options_scan.py -u http://192.168.1.0/24
    #""")
    option = OptionParser()
    option.add_option('-u', '--url', default=False, help='-u [http(s)://domain/ip(/mask length)]')
    option.add_option('-v', '--view', default=False, action='store_true', help='show more message')
    options, args = option.parse_args()
    global view
    view = options.view
    url = options.url
    if url == False and view == False:
        option.print_help()
        exit()
    print("Please wait...")
    return url

# 获取 HTTP Header
def getHTTPHead(url):
    requests.packages.urllib3.disable_warnings()                                # 忽略由于建立不安全的 https 连接导致 urllib3 库产生的警告
    try:
        response = requests.head(url, timeout = 3, verify=False)
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
        try:
            ips = IPy.IP(url.split("://")[1])
            scheme = url.split("://")[0] + "://"
            for ip in ips:
                urls.append(scheme + str(ip))
        except Exception as e:
            print('URL Error!')
    else:
        urls.append(url)
    return urls

# 将扫描结果写入字典
def oneScan(url):
    #lock.acquire()
    head = getHTTPHead(url)
    ips = IPy.IP(url.split("://")[1])
    sip = struct.unpack('>I', socket.inet_aton(str(ips)))[0]                    # 将 ip 转化为 int
    #lock.release()
    if head == "HTTPError!" and view == True:
        dic[sip] = "{:<30} {}".format("[-] " + url, "Dead Target/HTTP Error!")
    elif head == "HTTPError!" and view == False:
        pass
    else:
        status = dangerOptions(head)
        if status[1] == 0:
            # dic[sip] = "\033[32m{:<30} {:<40} {}\033[0m".format("[+] " + url, status[0], "HTTP Method Safe.")
            print("\033[32m{:<30} {:<40} {}\033[0m".format("[+] " + url, status[0], "HTTP Method Safe."))
        else:
            # dic[sip] = "\033[31m{:<30} {:<40} {}\033[0m".format("[+] " + url, status[0], "HTTP Method Dangerous!")
            print("\033[31m{:<30} {:<40} {}\033[0m".format("[+] " + url, status[0], "HTTP Method Dangerous!"))

def main():
    pool = ThreadPoolExecutor(max_workers=256)
    url = mainPage()
    urls = urlSplit(url)
    '''
    # wait 方法
    all_task = [pool.submit(oneScan, (url)) for url in urls]
    wait(all_task, return_when=ALL_COMPLETED)
    '''
    # map 方法
    for data in pool.map(oneScan, urls):
        pass
    for url in urls:
        t = threading.Thread(target = oneScan, args = (url,))                   # 多线程调用 oneScan() 扫描
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    for k in sorted(dic.keys()):                                                # 按 key 排序打印出字典中的 value
        print(dic[k])
        '''
    cgitb.enable(format='text')
    '''
    print("Down.")


if __name__ == "__main__":
    main()
