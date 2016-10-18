#-*- utf-8 -*-
from urllib.request import urlopen
import json

class Youdao():
    def __init__(self, word):
        self.word = word
        self.url = r'http://fanyi.youdao.com/openapi.do?keyfrom=<in put your from>&key=<input your key>&type=data&doctype=json&version=1.1&q=' + word

    @property
    def get_data(self):
        data = urlopen(self.url).read().decode('utf-8')
        data = json.loads(data)
        if data['errorCode']:
            print('error!')
            return
        try:
            basic = data['basic']
            web = data['web']
        except:
            return
        return (basic, web)

    def results(self, data):
        try:
            basic, web = data
        except:
            print('查无结果!')
            return
        print('\n音标:')
        print('US: %s  UK: %s' % (
                basic['us-phonetic'],
                basic['uk-phonetic'],
        ))
        print('\n基础解释:')
        for exp in basic['explains']:
            print(exp + '; ')
        print('\n网络解释:')
        for dicts in web:
            print(dicts['key'] + ' : ', end = '')
            for i in dicts['value']:
                print(i, end = '; ')
            print()

if __name__ == '__main__':
    while(True):
        try:
            word = input('\ninput a word:\n')
            if word.endswith(';'):
                break
            y = Youdao(word)
            y.results(y.get_data)
        except:
            break
