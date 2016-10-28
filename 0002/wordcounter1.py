#coding:utf-8
'''
by Jeffy
'''

from collections import Counter

def main():
    with open('text.txt', 'r', errors = 'ignore') as f:
        text = f.read()
        line_count = text.count('\n') + 1
        words_count = Counter(text.strip().split())
        for k, v in words_count.items():
            print("%s : %d" % (k, v))
            print("words:%d\nlines:%d" % (len(words_count), line_count))

if __name__ == '__main__':

    main()
