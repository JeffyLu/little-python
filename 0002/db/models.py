#coding:utf-8

from django.db import models

class WordList(models.Model):

    id = models.IntegerField(
        primary_key = True,
    )

    value = models.CharField(
        max_length = 26,
    )

    counts = models.IntegerField()

    def str(self):
        return self.value + '\t' + str(counts)
