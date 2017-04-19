#coding:utf-8

import os
import manage
import string
from django.db import transaction
from db.models import WordList
from collections import Counter

def words_counter():

    file_list = ['./textdata/' + f for f in os.listdir('./textdata')]
    for file_name in file_list:
        print('process %s...' % file_name)
        with open(file_name, 'r') as f:
            text = f.read()
        for s in string.punctuation:
            text = text.replace(s, ' ')
        text = text.replace('\n', ' ')
        yield Counter(text.split())

@transaction.atomic
def generate_wordlist():
    for words in words_counter():
        for value, counts in words.items():
            try:
                word = WordList.objects.get(
                    value = value
                )
                word.counts += count
            except:
                WordList.objects.create(
                    value = value,
                    counts = counts,
                )
        print('total:%d' % len(words))
        print('Done!')


if __name__ == '__main__':

    generate_wordlist()

