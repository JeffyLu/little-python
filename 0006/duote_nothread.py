#coding:utf-8

import re
import urllib.request

class DuoteSpyder:

    def __init__(self, url):
        self.url = url
        self.pages = 0
        self.apps = 0
        self.status = ''
        self.count_pages_and_apps()

    def count_pages_and_apps(self):
        response = urllib.request.urlopen(url % 1)
        content = response.read().decode('gbk')
        counts = re.findall(r'第\d/(.*?)页  共有：(.*?)条', content)
        try:
            self.pages, self.apps = map(int, counts[0])
        except Exception as e:
            print(e)

        print('本站包含{}个软件, 共有{}页'.format(self.apps, self.pages))

    def get_apps(self):
        for page in range(1, self.pages+1):
            try:
                response = urllib.request.urlopen(url % page, timeout=10)
                content = response.read().decode('gbk')
                self.status = '连接成功!'
            except:
                self.status = '连接失败!'

            info = self.__filter(content)
            with open('duote.txt', 'a') as f:
                for i in info:
                    app = '{0[2]}\t{0[3]}\t{0[0]}\t{0[1]}'.format(i)
                    #print(app)
                    f.write(app + '\n')

            print('爬取第{}页\t{}'.format(page, self.status))


    def __filter(self, content):
        pattern = re.compile(
            r'''>(人气.*?)<.*?>(好评率.*?)<.*?title="(.*?)".*?>(大小.*?)<''',
            re.S
        )
        info = re.findall(pattern, content)
        return info

    def run_spyder(self):
        self.get_apps()

if __name__ == '__main__':

    url = 'http://www.duote.com/sort/50_0_wdow_0_%d_.html'
    spyder = DuoteSpyder(url)
    spyder.run_spyder()
