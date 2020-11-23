#!/usr/bin/env python3
# super ping v0.1

import json
import requests
from fake_useragent import UserAgent

def getJSON(host, node):
    api_url = "https://www.wepcc.com/check-ping.html"
    data = {
        "node" : node,
        "host" : host
        }
    ua = UserAgent()
    fakeua={"User-Agent" : ua.random}
    requests.packages.urllib3.disable_warnings()                                # 忽略由于建立不安全的 https 连接导致 urllib3 库产生的警告
    try:
        response = requests.post(api_url, data = data, timeout = 50, headers = fakeua)
        response.raise_for_status()
        return response.content.decode('utf-8')
    except:
        return 0

def getIP(json_data):
    data = json.loads(json_data)["data"]
    ip = data["Ip"]
    return ip

def main():
    host = "www.781889.com"
    for node in range(1, 100):
        json_data = getJSON(host, node)
        if json_data == 0:
            pass
        else:
            ip = getIP(json_data)
            print(ip)

            

if __name__ == "__main__":
    main()