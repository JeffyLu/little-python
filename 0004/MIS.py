#-*- coding:utf-8 -*-
'''
by Jeffy
'''

import re
import os

class MIS(object):

    #initial
    def __init__(self):
        self.information = []
        self.menuid = ''
        self.filename = 'records.db'

    #file operator    
    def fileop(self, typeid, keyword = ''):
        with open(self.filename, 'a+') as f:
            
            #add
            if typeid == 1:
                f.write(self.information[0])
                for i in self.information[1:]:
                    f.write(',' + i)
                f.write('\n')
                return True
            
            #get all
            elif typeid == 21 or typeid == 22:
                count = 0
                f.seek(0)
                for line in f:
                    temp = line.strip('\n').split(',')
                    if typeid == 21:
                        count += 1
                        print(str(count) + '. ', end = '')
                        for i in temp:
                            print(i + '\t', end = '')
                        print()
                        continue
                    if len(temp) > 2:
                        count += 1
                        print(str(count) + '. ' + temp[2] + '\t' + temp[1])
                return count
            
            #search
            else:
                pattern = keyword
                regex = re.compile(pattern)
                f.seek(0)
                count = 0
                for line in f:
                    match = regex.search(line)
                    if match:
                        count += 1
                        print(str(count) + '. ' + line, end = '')
                return count
            
    def print1(self):
        print('\n*****results*****')
        print('total:%d\n' % self.fileop(21))
        
    def print2(self):
        print('\n*****results*****')
        print('total:%d\n' % self.fileop(22))
    
    def search(self):
        keyword = input('input key word:')
        print('\n*****results*****')
        print('total:%d\n' % self.fileop(23, keyword))
    
    def add(self):
        print('\n*****input information*****')
        self.information.append(input('employee payroll number:'))
        self.information.append(input('telephone number:'))
        self.information.append(input('name:'))
        self.information.append(input('department number:'))
        self.information.append(input('job title:'))
        self.information.append(input('date of hiring:'))
        if self.fileop(1):
            print('successful!')
        
    def delete(self):
        uid = input('employee payroll number to del:')
        with open(self.filename, 'r') as f:
            with open(self.filename + '.bak', 'w') as fb:
                for line in f:
                    if line.startswith(uid):
                        continue
                    fb.write(line)
        os.rename(self.filename, 'temp')
        os.rename(self.filename + '.bak', self.filename)
        os.rename('temp', self.filename + '.bak')
        
    def menu(self):
        print ('''Adfaith Consulting - Employee Information - Main Menu
=====================================================

1 - Print All Current Records
2 – Print Names and Phone Numbers
3 - Search for specific Record(s)
4 - Add New Records
5 – Delete Records

q - Quit\n''')
        self.menuid = input("Your Selection:")
        if not(self.menuid >= '1' and self.menuid <= '7' or self.menuid == 'q'):
            print ('input error!')
            self.menu()
        if self.menuid == '1':
            self.print1()
        elif self.menuid == '2':
            self.print2()
        elif self.menuid == '3':
            self.search()
        elif self.menuid == '4':
            self.add()
        else:
            self.delete()
            
    def run(self):
        while self.menuid != 'q':
            self.menu()

            
if __name__ == '__main__':
    
    mis = MIS()
    mis.run()
    
