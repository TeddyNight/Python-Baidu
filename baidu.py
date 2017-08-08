#!/bin/python
#-*-coding: utf-8-*-

import urllib
import urllib2
import cookielib
import re
import sys
# import random

fp = open('Result.html','a+')

class NoRedirection(urllib2.HTTPErrorProcessor):
  def http_response(self, request, response):
    return response
  https_response = http_response

class baidu_Search:

    def __init__(self):
        self.enable = True
        self.page = 0
    
    def rmTags(self,str):
        pattern1 = re.compile(r'<.*?>',re.DOTALL)
        pattern2 = re.compile(r'&nbsp')
        pattern3 = re.compile(ur';-;')
        pattern4 = re.compile(ur'&gt;\s*')
        str = pattern1.sub('',str)
        str = pattern2.sub('',str)
        str = pattern3.sub(u',',str)
        str = pattern4.sub(u'',str)
        return str
        
    def getPageCounts(self,htmlunicode):
        # <div class="nums">百度为您找到相关结果约68,900,000个</div>
        pattern = re.compile(r'<div class="nums">.+?</div>(.*?)</div>')
        m = pattern.search(htmlunicode)
        pagesCount = ''
        if m:
            pagesCount = m.group(1)    
        else:
            print u'不好意思,未查询到任何结果!'     
        return pagesCount
            
    def getNextPageUrl(self,htmlunicode):
        #pattern = re.compile(r'<div id="page"\s*>.*?<strong>.*?</strong><a href="(.*?)">')
        #m = pattern.search(htmlunicode)
        try:
           a = htmlunicode.index(u'下一页')
           c = htmlunicode.index('<div id="page" >')
           b = htmlunicode[c:a-12].split('"')
           m = b[int(len(b)-1)]
        except:
           m = ""
        nextPageUrl = ''
        if (m!=""):
            nextPageUrl = 'http://www.baidu.com' + m
        else:
            print u"未找到下一页"
        return nextPageUrl
        
    def getTitles_Abstracts(self,htmlunicode):
        patternResults = re.compile(r'<div class="result c-container\s*".*?><h3 class="t"\s*>.*?<div class="c-abstract"\s*>.*?</div>',re.DOTALL)
        # findall在无分组时返回元素为整个匹配字符串的list,在有分组时返回tuple类型的list
        m = patternResults.findall(htmlunicode)
        titles_abstracts = []
        if (m):
            # print m
            for result in m:
                patternTA = re.compile(r'<h3 class="t"\s*>(.*?)</h3>.*?<div class="c-abstract">(.*?)</div>',re.DOTALL)
                mTA = patternTA.search(result)
                if (mTA):
                    title = self.rmTags(mTA.group(1))
                    abstract = self.rmTags(mTA.group(2))
                    a = htmlunicode.find(title)
                    b = htmlunicode.find('<a target="_blank"',a)
                    c = htmlunicode.find('>',b)
                    opener = urllib2.build_opener(NoRedirection)
                    try:
                       location = opener.open(htmlunicode[b+25:c-49]).info().getheader('Location')
                       fp.writelines(location+'\n')
                       #print location
                    except:
                       location = '链接读取失败'
                    titles_abstracts.append((title,abstract,location))
                else:
                    titles_abstracts.append((u'没有标题',u'没有摘要',u'没有链接'))
        else:
            print u'为匹配到标题和摘要'           
        return titles_abstracts
        
    def Search(self,kw):
        kw = kw.decode(sys.stdin.encoding).encode('utf-8')
        searchurl = 'http://www.baidu.com/'+'s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd='+urllib.quote(kw)
        cj = cookielib.CookieJar();
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
        urllib2.install_opener(opener)
        req = urllib2.Request(searchurl)
        """user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
                        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) /Chrome/28.0.1468.0 Safari/537.36',
                        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)'
                        ]
        r = random.randint(0,7)
        req.add_header('User-agent',user_agents[r])
        """
        resp = urllib2.urlopen(req) 
        htmlunicode = resp.read().decode('utf-8')
        
        #print htmlunicode
        #myfile = open('text.txt','w')
        #myfile.write(htmlunicode.encode('utf-8'))
        pagesCount = self.getPageCounts(htmlunicode)
        print pagesCount

        while self.enable:
            if(len(sys.argv)==3):
               if(int(sys.argv[2]) > self.page):
                  print u'正在浏览第',self.page+1,'页'
               else:
                  break
            else:
               print u'请按[回车键]浏览第',self.page+1,'页内容,输入[quit]退出程序:'
               myInput = raw_input()
               if (myInput== 'quit'):
                   break  
            titles_abstracts = self.getTitles_Abstracts(htmlunicode)
            for index in range(len(titles_abstracts)):
                print u"第",self.page+1,"页第",index+1,"个搜索结果..."
                print u"标题: ",titles_abstracts[index][0]
                print u"摘要: ",titles_abstracts[index][1]
                print u"链接: ",titles_abstracts[index][2]
                print "\r\n"
                
            nextPageUrl = self.getNextPageUrl(htmlunicode)
            self.page += 1
            # print u'下一页url为:', nextPageUrl
            if (nextPageUrl == ''):
                break
            resp = urllib2.urlopen(nextPageUrl)
            htmlunicode = resp.read().decode('utf-8')
            
if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print u"""
--------------------------------------------
author: Ted
date  : 2017-08-08
howTo : python baidu.py keyword ,enter "quit" to quit program
advert: python baidu.py 关键词 ，按下任意键来浏览,按下quit退出
--------------------------------------------
        """
    else:
        myBaidu = baidu_Search()
        myBaidu.Search(sys.argv[1])
    fp.close()
