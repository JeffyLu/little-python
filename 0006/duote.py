# -*- coding:gbk -*-
import re
import urllib2

class pachong:
    def __init__(self):
        self.pageIndex = 1
        self.num = 1
        self.user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
      #  self.softwaresname = []
        
    def getPage(self, pageIndex):
        print 'page %d' % pageIndex
        url = 'http://www.duote.com/sort/50_0_wdow_0_' + str(pageIndex) + '_.html'
        request = urllib2.Request(url, headers = self.headers)
        response = urllib2.urlopen(request)
        pageCode = response.read()
        return pageCode
    
    def getPageItems(self):
        pageCode = self.getPage(self.pageIndex)
        if self.pageIndex == 1:
            pattern = re.compile(r'<span class="count">.*?[0-9]/([0-9]*[1-9][0-9]*)')
            num = re.findall(pattern, pageCode)
            self.num = int(num[0])
            #print int(num[0])
        self.pageIndex += 1
        pattern = re.compile(r'<a onclick=.*?l211.*?title="(.*?)">.*?</a>')
        title = re.findall(pattern, pageCode)
        return title
    
    def getTitle(self):
        f = open("software.txt", 'w+')
        count = 1
        while self.pageIndex <= self.num:
            for i in self.getPageItems():
                temp = str(count) + '、' + i + '\n'
                f.write(temp)
                count += 1
        print 'over!'
        f.close()
spider = pachong()
spider.getTitle()
