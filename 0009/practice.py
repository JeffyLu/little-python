#-*- coding:utf-8 -*-
'''
by Jeffy
'''

def main():
    while(True):
        string = str(input('input string:'))
        if not string:
            break
        string1 = list(string)
        string1.reverse()
        string1 = ''.join(string1)
        if string == string1:
            print('yes')
        else:
            print('no')

if __name__ == '__main__':
    main()
