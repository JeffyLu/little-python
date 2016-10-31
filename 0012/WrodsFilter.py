#coding:utf-8
'''
by Jeffy
'''

def main():
    with open('filtered_words.txt', 'r') as f:
        text = str(input('input text:'))
        filter_word = f.read().strip().split('\n')
        for word in filter_word:
            if word in filter_word:
                text = text.replace(word, '*'*len(word))
        print('output text:' + text)

if __name__ == '__main__':

    main()
