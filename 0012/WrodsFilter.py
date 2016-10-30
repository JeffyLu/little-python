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
                replace = ['*' for i in range(len(word))]
                text = text.replace(word, ''.join(replace))
        print('output text:' + text)

if __name__ == '__main__':

    main()
