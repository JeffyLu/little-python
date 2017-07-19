# coding:utf-8

from collections import Counter


def main(filename):
    symbols = list('.,-\\/"\'![]()“”')
    with open(filename, 'r') as f:
        context = f.read().lower()
        for s in symbols:
            context = context.replace(s, ' ')
        lines = context.count('\n')
        words = []
        for line in context.strip().split('\n'):
            words += line.strip().split(' ')
        counter = Counter(words)
        for k, v in counter.items():
            print('%s : %s' % (k, v))
        print('lines : %d' % lines)
        print('words : %d' % len(counter))

if __name__ == '__main__':

    main('car-child-soldiers.txt')
