# -*- coding: utf-8 -*-
# coding: utf-8

import re
import os
import sys
# import xbmc
import urllib

import zipfile
import requests


# import requests
import shutil
# import xbmcvfs
# import xbmcaddon
# import xbmcgui,xbmcplugin
from bs4 import BeautifulSoup

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

page = requests.get('http://www.subku.net/dld/1049.html')
soup = BeautifulSoup(page.text,'html.parser')
div = soup.find('div',class_='down clearfix')
li = div.find('li')

headers['Referer'] = 'http://www.subku.net/dld/1049.html'
page = requests.get(li.a.get('href'),headers=headers)
print(page.headers['Content-Disposition'])