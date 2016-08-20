#-*- coding:utf-8 -*-
import re

filename = 'text.txt'
wordcount = 0
linecount = 0
worddict = {}

with open(filename, 'r') as f:
    for line in f:
        words = re.findall(r'[a-zA-Z0-9]+', line)
        linecount += 1
        for i in words:
            if i not in worddict:
                worddict[i] = 1
            else:
                worddict[i] += 1
    wordcount = len(worddict)

for k, v in worddict.items():
    print(k, v)

print ("\nlines:%d\nwords:%d" % (linecount, wordcount))
        
