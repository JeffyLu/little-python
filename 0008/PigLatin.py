#-*- coding:utf-8 -*-
'''
by Jeffy
'''

import string
    
def main():
    alph = [i for i in 'aeiou']
    word = input("input a word:")
    if word[0].lower() not in alph:
        word = word[1:] + '-' + word[0] + 'ay'
        print(word)
    else:
        print('input another one!')
        main()

if __name__ == '__main__':
    main()
