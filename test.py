# -*- coding: utf-8 -*-

import re
import os
import sys
# import xbmc
import urllib
import urllib2
# import requests
import shutil
# import xbmcvfs
# import xbmcaddon
# import xbmcgui,xbmcplugin
from bs4 import BeautifulSoup

# class NoRedirection(urllib2.HTTPErrorProcessor):
#     """docstring for NoRedirection"""
#     def http_response(self, request, response):
#         return response
#     https_respoonse = http_response
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}



ZIMUKU_API = 'http://www.zimuku.net/search?q=%s'
ZIMUKU_BASE = 'http://www.zimuku.net'
FLAG_DICT = {'china':'简', 'hongkong':'繁', 'uk':'英', 'jollyroger':'双语'}

def Search():
    subtitles_list = []

    # log( __name__ ,"Search for [%s] by name" % (os.path.basename( item['file_original_path'] ),))
    # if item['mansearch']:
    #     url = ZIMUKU_API % '最终幻想15：王者之剑'
    # else:
    url = ZIMUKU_API % '最终幻想15：王者之剑'
    try:
        socket = urllib.urlopen(url)
        data = socket.read()
        socket.close()
        soup = BeautifulSoup(data,'html.parser')
    except:
        return
    results = soup.find_all("div", class_="item prel clearfix")
    for it in results:
        moviename = it.find("div", class_="title").a.text.encode('utf-8')
        iurl = it.find("div", class_="title").a.get('href').encode('utf-8')
        movieurl = '%s%s' % (ZIMUKU_BASE, iurl)
        try:
            print(movieurl)
            socket = urllib.urlopen(movieurl)
            data = socket.read()
            socket.close()
            soup = BeautifulSoup(data,'html.parser').find("table", class_="table")
            soup = soup.find("tbody")
        except:
            return
        subs = soup.find_all("tr")
        for sub in subs:
            name = sub.a.text.encode('utf-8')
            imgs = sub.find_all('img')
            flag = sub.img.get('src').split('/')[-1].split('.')[0].encode('utf-8')
            lang = FLAG_DICT.get(flag,'unkonw')

            for img in imgs: flags.append(img.get('src').split('/')[-1].split('.')[0].encode('utf-8'))
            link = '%s%s' % (ZIMUKU_BASE, sub.a.get('href').encode('utf-8'))

            if lang == '英':
                subtitles_list.append({"language_name":"English", "filename":name, "link":link, "language_flag":'en', "rating":"0", "lang":lang})
            else:
                subtitles_list.append({"language_name":"Chinese", "filename":name, "link":link, "language_flag":'zh', "rating":"0", "lang":lang})


    if subtitles_list:
        for it in subtitles_list:
            listitem = xbmcgui.ListItem(label=it["language_name"],
                                  label2=it["filename"],
                                  iconImage=it["rating"],
                                  thumbnailImage=it["language_flag"]
                                  )

            listitem.setProperty( "sync", "false" )
            listitem.setProperty( "hearing_imp", "false" )

            url = "plugin://%s/?action=download&link=%s&lang=%s" % (__scriptid__,
                                                                        it["link"],
                                                                        it["lang"]
                                                                        )
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=listitem,isFolder=False)

def Download():
    # try: shutil.rmtree(__temp__)
    # except: pass
    # try: os.makedirs(__temp__)
    # except: pass

    subtitle_list = []
    exts = [".srt", ".sub", ".smi", ".ssa", ".ass" ]
    try:
        socket = urllib.urlopen('http://www.zimuku.net/detail/76176.html')
        data = socket.read()
        soup = BeautifulSoup(data,'html.parser')
        url = soup.find("li", class_="li dlsub").a.get('href').encode('utf-8')
        socket = urllib.urlopen(url)

        data = socket.read()
        soup = BeautifulSoup(data,'html.parser')
        div = soup.find('div',class_='down clearfix')
        li = div.find('li')
        headers['Referer'] = url

        req = urllib2.Request(li.a.get('href'),headers=headers)
        resp = urllib2.urlopen(req)
        socket = urllib.urlopen(resp.geturl())
        data = socket.read()
        socket.close()
    except:
        return []

    if len(data) < 1024:return []

    # tempfile = os.path.join(__temp__, "subtitles%s" % os.path.splitext(filename)[1])
    tempfile = li.a.text+'.zip'

    with open(tempfile, "wb") as subFile: subFile.write(data)
    subFile.close()
    return


    xbmc.sleep(500)
    if data[:4] == 'Rar!' or data[:2] == 'PK':
        xbmc.executebuiltin(('XBMC.Extract("%s","%s")' % (tempfile,__temp__,)).encode('utf-8'), True)
    path = __temp__
    dirs, files = xbmcvfs.listdir(path)
    if len(dirs) > 0:
        path = os.path.join(__temp__, dirs[0].decode('utf-8'))
        dirs, files = xbmcvfs.listdir(path)
    list = []
    for subfile in files:
        if (os.path.splitext( subfile )[1] in exts):
            list.append(subfile.decode('utf-8'))
    if len(list) == 1:
        subtitle_list.append(os.path.join(path, list[0]))
    else:
        sel = xbmcgui.Dialog().select('请选择压缩包中的字幕', list)
        if sel == -1:
            sel = 0
        subtitle_list.append(os.path.join(path, list[sel]))

    return subtitle_list

Search()
# Download()

