#-*- coding:utf-8 -*-
'''
by Jeffy
'''

import string
    
def main():
    alph = [i for i in 'aeiou']
    word = str(input("input a word:"))
    if not word.isalpha():
        print("input another one!")
        return
    if word[0].lower() not in alph:
        word = word[1:] + '-' + word[0] + 'ay'
        print(word)
    else:
        print('input another one!')
        return

if __name__ == '__main__':
    while(True):
        try:
            main()
        except:
            break
