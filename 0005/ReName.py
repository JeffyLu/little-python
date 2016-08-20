#-*- coding:utf-8 -*-
'''
by Jeffy
'''

import os
import sys

class ReName(object):
    def __init__(self):
        self.path = '.'
        self.filetype = ''
        self.newfiletype = ''
        self.errorlist = []
        
    #input filetype && path    
    def input(self, flag = True):
        print('current directory:' + os.getcwd())
        while flag:
            self.path = input('input path(pardir ..|curdir .):')
            if os.path.exists(self.path):
                flag = False
                os.chdir(self.path)
        while not(self.filetype.startswith('.') and \
              self.filetype[1:].isalnum()):
            self.filetype = input('input filetype(like .jpg):')
        self.newfiletype = input("input newfiletype('enter' to del filetype):")
        print('\ncurrent working directory: %s\nfiletype: *%s\nnewfiletype: *%s'\
              % (os.getcwd(), self.filetype, self.newfiletype))

    #confirm information
    def confirm(self):
        print('\nchanging *%s to *%s\nare you sure?' % (self.filetype, self.newfiletype))
        print('Y to continue, N to input again, Q to quit:')
        while True:
            temp = input('Y|N|Q :').lower()
            if temp == 'y':
                return True
            elif temp == 'n':
                os.chdir(sys.path[0])
                self.__init__()
                return False
            elif temp == 'q':
                os._exit(0)
            else:
                print('input error!')
                
    #rename        
    def rename(self):
        count = 0
        for file in os.listdir():
            if file.endswith(self.filetype):
                try:
                    count += 1
                    newfile = file[:-len(self.filetype)] + self.newfiletype
                    os.rename(file, newfile)
                    print("%d. %s    -->    %s    done" % (count, file, newfile))
                except:
                    print("%d. %s    -->    %s    error" % (count, file, newfile))
                    self.errorlist.append(file)
                    continue                
        print('statistic:\ntotal:%d  succeed:%d  error:%d' \
              % (count, count - len(self.errorlist), len(self.errorlist)))
        while self.errorlist:
            temp = input("input 'S' to show error list 'Q' to quit:").lower()
            if temp == 's':
                count = 0
                for i in self.errorlist:
                    count += 1
                    print('%d. %s' % (count, i))
            elif temp == 'q':
                os._exit(0)
            else:
                print('input error!')
                
    def run(self):
        self.input(1)
        while not self.confirm():
            self.input(1)
        self.rename()
        os.system('pause')            
    
if __name__ == '__main__':

    runner = ReName()
    runner.run()
