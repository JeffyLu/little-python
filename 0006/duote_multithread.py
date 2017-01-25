#coding:utf-8

import re
import time
import queue
import threading
import urllib.request

class ThreadSpyder(threading.Thread):

    def __init__(self, name, url, queue):
        threading.Thread.__init__(self)
        self.setName(name)
        self.url = url
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            page = self.queue.get()
            status = self.get_apps(page)
            self.queue.task_done()
            print('{}  爬取第{}页\t{}'.format(self.getName(), page, status))

    def get_apps(self, page):
        try:
            response = urllib.request.urlopen(self.url % page, timeout=10)
            content = response.read().decode('gbk')
        except:
            return False

        info = self.__filter(content)
        with open('duote.txt', 'a') as f:
            for i in info:
                app = '{0[2]}\t{0[3]}\t{0[0]}\t{0[1]}'.format(i)
                f.write(app + '\n')
        return True

    def __filter(self, content):
        pattern = re.compile(
            r'''>(人气.*?)<.*?>(好评率.*?)<.*?title="(.*?)".*?>(大小.*?)<''',
            re.S
        )
        info = re.findall(pattern, content)
        return info


class DuoteSpyder:

    def __init__(self, url):
        self.url = url
        self.pages = 0
        self.apps = 0
        self.count_pages_and_apps()

    def count_pages_and_apps(self):
        response = urllib.request.urlopen(self.url % 1)
        content = response.read().decode('gbk')
        counts = re.findall(r'第\d/(.*?)页  共有：(.*?)条', content)
        try:
            self.pages, self.apps = map(int, counts[0])
        except Exception as e:
            print(e)

        print('本站包含{}个软件, 共有{}页'.format(self.apps, self.pages))

    def run_spyder(self):
        start_time = time.time()

        q = queue.Queue()
        for page in range(1, self.pages+1):
            q.put(page)

        threads = []
        for i in range(4):
            thread = ThreadSpyder(i, self.url, q)
            thread.daemon = True
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()

        print(time.time() - start_time)

if __name__ == '__main__':

    url = 'http://www.duote.com/sort/50_0_wdow_0_%d_.html'
    spyder = DuoteSpyder(url)
    spyder.run_spyder()
