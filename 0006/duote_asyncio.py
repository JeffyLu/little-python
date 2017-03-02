#coding:utf-8

import re
import requests
import aiohttp
import asyncio
import time



url = "http://www.duote.com/sort/50_0_wdow_0_%d_.html"

async def get_body(url):
    response = await aiohttp.request('GET', url)
    return await response.read()

async def handle_task(task_id, work_queue):
    while not work_queue.empty():
        status = False
        try:
            p = await work_queue.get()
            body = await get_body(url % p)
            parser(body.decode('gbk', errors = 'ignore'))
            status = True
        except Exception as e:
            print(e)
        finally:
            print('{}  爬取第{}页\t{}'.format(task_id, p, status))

def parser(content):
    pattern = re.compile(
        r'''>(人气.*?)<.*?>(好评率.*?)<.*?title="(.*?)".*?>(大小.*?)<''',
        re.S
    )
    info = re.findall(pattern, content)
    with open('duote.txt', 'a') as f:
        for i in info:
            app = '{0[2]}\t{0[3]}\t{0[0]}\t{0[1]}'.format(i)
            f.write(app + '\n')

def main():
    start = time.time()
    q = asyncio.Queue()

    response = requests.get(url % 1)
    counts = re.findall(r'第\d/(.*?)页  共有：(.*?)条', response.text)
    pages, apps = map(int, counts[0])

    [q.put_nowait(p) for p in range(1, pages + 1)]
    loop = asyncio.get_event_loop()
    tasks = [handle_task(task_id, q) for task_id in range(8)]
    print('本站包含{}个软件, 共有{}页'.format(apps, pages))
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print(time.time()-start)


if __name__ == "__main__":

    main()
