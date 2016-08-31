#-*- coding:utf-8 -*-

'''
by Jeffy
'''

import itertools
import time

def cube3(i):
    a = i[0] + i[1] + i[2]
    b = i[3] + i[4] + i[5]
    if a == b:
        b = i[6] + i[7] + i[8]
    else:
        return False
    if a == b:
        b = i[0] + i[3] + i[6]
    else:
        return False
    if a == b:
        b = i[1] + i[4] + i[7]
    else:
        return False
    if a == b:
        b = i[2] + i[5] + i[8]
    else:
        return False
    if a == b:
        b = i[0] + i[4] + i[8]
    else:
        return False
    if a == b:
        b = i[2] + i[4] + i[6]
    else:
        return False
    return True

def main():
    count = 0  
    start = time.time()
    for i in itertools.permutations(range(1, 10), 9):
        if cube3(i):
            count += 1
            flag = 1
            print('result %d:' % (count))
            for k in i:
                print('%d ' % (k), end = '')
                if not(flag % 3):
                    print()
                flag += 1     
    end = time.time()
    print('time:', end - start)
    print('total:', count)

if __name__ == '__main__':

    main()
