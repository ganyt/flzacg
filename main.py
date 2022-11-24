import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time
from retry import retry
import os

@retry(tries=64)
def urlget(url):
    proxy='127.0.0.1:2333'
    proxies={
    'http':'http://'+proxy,
    'https':'http://'+proxy
    }
    #####定义好请求头#####
    cookies = {
    'timezone': '8',
    }

    headers = {
    'authority': 'od.lzacg.one',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'timezone=8',
    #'referer': url,
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
    }

    requests.DEFAULT_RETRIES = 35
    response = requests.get(url, cookies=cookies, headers=headers, proxies=proxies, timeout=300)
    purl = (response.text)
    print("正在获取"+url)
    return purl

def reahref(url,html_str):
    path=[]
    file=[]
    dic = {"path":path,"file":file}
    bs = BeautifulSoup(html_str,"html.parser")
    dir = bs.find_all('a', {'name': 'folderlist'})
    if not len(dir)==0:
        for r in dir:
            #print(r)
            res = re.findall('(.*)href="(.*?)" (.*)',str(r))
            result = res[0]
            caurl = unquote(url)
            fullurl = caurl + str(result[1])
            path.append(fullurl)
    dirf = bs.find_all('a', {'class': 'download'})
    print(dirf)
    for r in dirf:
        print(r)
        a = re.compile('<a class="download" href="(.+)"><ion-icon name="download"></ion-icon></a>')
        res = a.findall(str(r))
        result = res[0]
        caurl = unquote(url)
        fullurl = caurl + result
        file.append(fullurl)

    return dic

def analyzeurl(url):
    ###########处理url地址，从中获得文件名和文件路径
    apath = re.compile('https://.*.lzacg.one/(.+)/.*$')
    respath = apath.findall(str(url))
    filepath = "/" + respath[0] + "/"
    afilename = re.compile('https://.*.lzacg.one/.*/(.+?)$')
    resfilename = afilename.findall(str(url))
    filename = resfilename[0]
    filesim = {"url": url, "filepath": filepath, "filename": filename}
    jsonstr = json.dumps(filesim)
    # print(jsonstr)
    with open("/disk/path/odb.lzacg.json", "a") as f:
        f.write(jsonstr + "\n")


def fuckurl(rooturl):
    htmlstr=urlget(rooturl)
    filedic = reahref(rooturl,htmlstr)
    urllist=filedic["path"]
    print(urllist)
    fileurllist=filedic["file"]
    print(fileurllist)
    for url in urllist:
        time.sleep(5)
        print(url)
        fuckurl(url)
    for fileurl in fileurllist:
        analyzeurl(fileurl)

def fuckmainurl(rooturl):
    htmlstr=urlget(rooturl)
    filedic = reahref(rooturl,htmlstr)
    #urllist=filedic["path"]
    jsonstr = json.dumps(filedic["path"])
    with open("/disk/path/odb.list.json", "a") as f:
        f.write(jsonstr + "\n")

def fucklisturl():
    for line in open("/disk/path/odb.list.json"):
        urllist = json.loads(line)
        for url in urllist:
            print("Fuck"+url)
            time.sleep(15)
            fuckurl(url)



fuckmainurl("https://odb.lzacg.one/")
#fucklisturl()