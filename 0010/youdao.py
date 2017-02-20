#-*- utf-8 -*-
'''
by Jeffy
'''

from urllib.request import urlopen
from urllib.parse import urlencode
import json

class Youdao():

    def __init__(self):
        self.url = r'http://fanyi.youdao.com/openapi.do?'
        self.explain = {
            'translation' : None,
            'phonetic' : None,
            'us-phonetic' :  None,
            'uk-phonetic' : None,
            'explains' : None,
            'web' : None,
        }
        self.postdata = {
            'keyfrom' : 'your keyfrom',
            'key' : 'your key',
            'type' : 'data',
            'doctype' : 'json',
            'version' : '1.1',
            'q' : None,
        }

    def parser(self, data):
        if 'translation' in data:
            self.explain['translation'] = data['translation']

        if 'basic' in data:
            for k, v in data['basic'].items():
                if k in self.explain:
                    self.explain[k] = v
        if 'web' in data:
            self.explain['web'] = data['web']

        print('\n------发    音------\n')
        print('%s  US: %s  UK: %s' % (
                self.explain['phonetic'],
                self.explain['us-phonetic'],
                self.explain['uk-phonetic'],
        ))
        if self.explain['translation']:
            print('\n------翻    译------\n')
            for i in self.explain['translation']:
                print(i + '; ', end = '')
            print()
        if self.explain['explains']:
            print('\n------基础解释------\n')
            for exp in self.explain['explains']:
                print(exp + '; ')
        if self.explain['web']:
            print('\n------网络解释------\n')
            for dicts in self.explain['web']:
                print(dicts['key'] + ' : ', end = '')
                for i in dicts['value']:
                    print(i, end = '; ')
                print()

    def main(self, word):
        self.postdata['q'] = word
        response = urlopen(self.url, urlencode(self.postdata).encode()).read()
        data = json.loads(response.decode('utf-8'))
        if data['errorCode']:
            print('error!')
            return False
        self.parser(data)

if __name__ == '__main__':

    app = Youdao()
    while(True):
        try:
            word = input("\n输入翻译内容(';'退出):\n\n")
            if word.endswith(';') or word.endswith('；'):
                break
            app.main(word)
        except:
            break
