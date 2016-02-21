import requests
import os
import re

#proxy_support = urllib.request.ProxyHandler({'http': 'http://localhost:1080'})
#print(proxy_support)
#opener = urllib.request.build_opener(proxy_support)
#print(opener)
#urllib.request.install_opener(opener)

#a = urllib.request.urlopen("https://www.youtube.com").read().decode("utf-8", errors="ignore")
#a = opener.open("http://www.ip138.com").read().decode("gb2312")
#print(a)

#print("done")

def getResp(url):
    session = requests.session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    session.proxies = {'http': 'http://127.0.0.1:10800', 'https': 'http://127.0.0.1:10800'}
    response = session.get(url)
    return response

def saveToFile(url, dir, num):
    filename = os.path.basename(url)
    fullname = dir + num + "_" + filename
    #print("saveToFile:" + filename + " || " + fullname)

    response = getResp(url)
    
    with open(fullname, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return

def saveToFileSetName(url, fullpath):
    response = getResp(url)
    
    with open(fullpath, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return
    return

#分析一个帖子
def getTitle(html):
    m2 = re.findall(r'<title>(.*)\|.*</title>', html)
    if m2:
        return m2[0]
    return "null"

def getImgs(html):
#    m2 = re.findall(r'postmessage[\s\S]*?img src=\"(.*?)\"[\s\S]*?postattachlist', html)
    m1 = re.findall(r'<div id=\"postmessage_([\s\S]*?)postattachlist', html)
    if m1:
        m2 = re.findall(r'src="(http://.*\.jpg)"', m1[0])
        return m2
    return m1

def getTorrent(html):
    m2 = re.findall(r'<a href=\"attachment\.php\?aid=(.*?)\"', html)
    if m2:
        return m2[0]
    return "null"

#分析每个帖子
def doThread(threadid, basePath):
    fullurl = "http://sis001.com/forum/thread-" + threadid + "-1-1.html"
    #print(fullurl)
    r = getResp(fullurl)
    html = r.content.decode(encoding="gbk", errors="ignore")
#    print(html)

    #获取标题
    #title = getTitle(html)
    #print(title)

    #获取图片列表
    piclst = getImgs(html)
    #print(piclst)

    #下载图片
    for picurl in piclst:
        saveToFile(picurl, basePath, threadid)

    #获取种子连接
    torr = getTorrent(html)
    #print(torr)
    
    #下载种子
    saveToFileSetName("http://sis001.com/forum/attachment.php?aid="+torr, basePath + threadid + ".torrent")
    return

#分析列表页,返回这个页面上所有正常帖子的id列表
def doList(url):
    r = getResp(url)
    html = r.content.decode(encoding="gbk", errors="ignore")

    m1 = re.findall(r'推荐主题([\s\S]*)个月以来主题', html)
    if m1:
        m2 = re.findall(r'thread-(.*?)-', m1[0])
        return list(set(m2))
    else :
        m1 = re.findall(r'版块主题([\s\S]*)个月以来主题', html)
        if m1:
            m2 = re.findall(r'thread-(.*?)-', m1[0])
            return list(set(m2))
        return m1

#循环获取每个帖子
def doMainList(lsturl, basePath):
    rrr = doList(lsturl)
    for threadnum in rrr:
        print("=", end = '')
        doThread(threadnum, basePath)

    print("|")
    return

#循环所有列表页
def exeMain(urllst, basePath):
    for url in urllst:
        print("Url:%s" %(url))
        doMainList(url, basePath)
    return

#saveToFile("http://i.imgur.com/o6SzpGV.jpg", "d:\\linshi\\python\\tmp\\")
#doThread("9590393", "d:\\linshi\\python\\tmp\\")
#rrr = doList("http://sis001.com/forum/forum-143-2.html")
#doMainList("http://sis001.com/forum/forum-143-2.html", "d:\\linshi\\python\\tmp\\")
#print(rrr)

urls=[]
urls.append("http://sis001.com/forum/forumdisplay.php?fid=143")
urls.append("http://sis001.com/forum/forum-143-2.html")
urls.append("http://sis001.com/forum/forum-143-3.html")
urls.append("http://sis001.com/forum/forum-143-4.html")
urls.append("http://sis001.com/forum/forum-143-5.html")
#urls[5] = "http://sis001.com/forum/forum-143-6.html"
#urls[6] = "http://sis001.com/forum/forum-143-7.html"
#urls[7] = "http://sis001.com/forum/forum-143-8.html"
#urls[8] = "http://sis001.com/forum/forum-143-9.html"
#urls[9] = "http://sis001.com/forum/forum-143-10.html"

exeMain(urls, "d:\\linshi\\python\\h\\")

print("All done")







