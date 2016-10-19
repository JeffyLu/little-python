#-*- utf-8 -*-
'''
by Jeffy
'''

from urllib.request import urlopen
from urllib.parse import urlencode
import json

class Youdao():
    def __init__(self, word):
        self.explain = {
            'translation' : None,
            'phonetic' : None,
            'us-phonetic' :  None,
            'uk-phonetic' : None,
            'explains' : None,
            'web' : None,
        }
        self.postdata = {
            'keyfrom' : 'your webfrom',
            'key' : 'your key',
            'type' : 'data',
            'doctype' : 'json',
            'version' : '1.1',
            'q' : word,
        }
        self.postdata = urlencode(self.postdata).encode()
        self.url = r'http://fanyi.youdao.com/openapi.do?'

    @property
    def get_data(self):
        data = urlopen(self.url, self.postdata).read()
        data = json.loads(data.decode('utf-8'))
        #print(data)
        if data['errorCode']:
            print('error!')
            return
        return data

    def results(self, data):
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


if __name__ == '__main__':
    while(True):
        try:
            word = input("\n输入翻译内容(';'退出):\n\n")
            if word.endswith(';'):
                break
            y = Youdao(word)
            y.results(y.get_data)
        except:
            break
