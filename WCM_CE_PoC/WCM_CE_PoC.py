#!/usr/bin/env python3
# TRS WCM code execution detection (WooYun-2013-34315 PoC)

import requests
import sys

if len(sys.argv) < 2:
    print("""
    WCM_CE_PoC.py
    TRS WCM code execution detection (WooYun-2013-34315 PoC)
    usage:
        python3 WCM_CE_PoC.py <URL>
    e.g.
        python3 WCM_CE_PoC.py http://www.xxx.com
        """)
else:   
    url = sys.argv[1] + "/wcm/services/trs:templateservicefacade?wsdl"
    try:
        response = requests.get(url, timeout = 30)
        response.raise_for_status()
        if "writeFile" in response.text or "writeSpecFile" in response.text:
            print("\033[31m[!] Find Vulnerabilities!\033[0m")
        else:
            print("\033[32m[!] Safe\033[0m")
    except:
        print("\033[33m[!] HTTP Error!\033[0m")