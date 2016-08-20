#-*- coding:utf-8 -*-
'''
by Jeffy
'''

import os

def findfile(path):
    filelist = []
    for filename in os.listdir(path):
        filelist.append(filename)
        #print (filelist)
    return filelist

def stat(path):
    filelist = findfile(path)
    line_total = 0
    for i in filelist:
        emptyline_count = 0
        noteline_count = 0
        line_count = 0
        with open(path + '\\' + i, 'r') as f:
            noteflag = 0
            for line in f:
                temp = line.split()
                if noteflag:
                    if temp[-1].endswith('*/'):
                        noteflag = 0
                    noteline_count += 1
                    continue
                if not temp:
                    emptyline_count += 1
                    continue
                elif temp[0].startswith('/'):
                    if temp[0].startswith('//'):
                        noteline_count += 1
                        continue
                    else:
                        noteflag = 1
                        noteline_count += 1
                else:
                    line_count += 1
                
        print ("filename:%s lines:%d notelines:%d emptylines:%d" % \
               (i, line_count, noteline_count, emptyline_count))
        line_total += line_count + noteline_count + emptyline_count
    print ("total lines:%d" % line_total)
    
if __name__ == '__main__':
    stat('./code')
