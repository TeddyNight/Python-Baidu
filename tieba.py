# -*- coding:utf-8 -*--
import urllib
import urllib2
import thread
import time
file = open("result","w")
pnum = "1"
kw = urllib.quote("免费空间")
baseurl = 'https://tieba.baidu.com/mo/q---1EAA77E05F1AE3EFF64D6BE45DD8ADF8%3AFG%3D1--1-3-0--2--wapp_1503934250237_446/'
def get_page(url):
  req = urllib2.Request(baseurl+url)
  src = urllib2.urlopen(req).read()
  e = src.find('<a href="http://gate.baidu.com')
  if (e != -1):
    f = src.find('src=',e)
    g = src.find('">',e)
    try:
      req = urllib2.Request(urllib.unquote(src[f+4:g]))
      handle = urllib2.urlopen(req,timeout=3)
      src = handle.read()
      link = handle.geturl()
    except:
      return 0
    h = src.find('<title>')
    if (h != -1):
      i = src.find('</title>')
      print link+' '+src[h+7:i]
      file.write(link+' '+src[h+7:i]+'\n')
req = urllib2.Request(baseurl+'m?pnum='+pnum+'&lm=&kw='+kw)
res = urllib2.urlopen(req).read()
p1 = res.find('第1/')
p2 = res.find('页',p1)
page = res[p1+5:p2]
while (pnum != page):
   print '正在抓取第'+pnum+'页'
   req = urllib2.Request(baseurl+'m?pnum='+pnum+'&lm=&kw='+kw)
   res = urllib2.urlopen(req).read()
   c = 0
   while True:
     a = res.find('class="i"',c)
     if (a == -1):
       break
     b = res.find('<a href="',a)
     c = res.find('">',b)
     thread.start_new_thread(get_page,(res[b+9:c],))
     #get_page(res[b+9:c])
   pnum = str(int(pnum)+1)
time.sleep(5)
