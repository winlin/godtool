#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import time
import urllib2
import subprocess
import simplejson as json
from datetime import datetime
from bs4 import BeautifulSoup


if len(sys.argv)!=3:
    print 'Usage:%s target_url minprice' % (sys.argv[0])
    sys.exit(1)

def printlog(msg):
    print datetime.now(), msg

tar_url, min_price = sys.argv[1], sys.argv[2]

while True:
    printlog('Going to min_price:%s fetch:%s' % (min_price, tar_url))
    try:
        page = urllib2.urlopen(tar_url)
        soup = BeautifulSoup(page, "html.parser")
        result = soup.findAll('div', {'class':'can-buy-count'})
        printlog(result)
        p_list = []
        for item in result:
            price = re.compile(r'[1-9]\d*\.*\d*').findall(str(item))
            if price:
                p_list.append(float(price[0]))
        p_list = sorted(p_list)
        printlog("\nget print list %s\n" % p_list)
        if p_list and p_list[0] < float(min_price):
            printlog("$$$$$$$ get min price %f" % p_list[0])
            cmd_line = '''osascript -e 'display notification "$$$ Find Min Price $$$" with title "%f"' ''' % p_list[0]
            subprocess.call(cmd_line, shell=True)
    except Exception as e:
        print str(e)
    time.sleep(3)


