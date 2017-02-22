from django.db import models
from django.conf import settings
# Create your models here.

class Mylist(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )

    item = models.TextField(
        max_length = 200,
    )

    status = models.BooleanField(
        default = False,
    )

    class Meta:

        verbose_name = 'To Do List'
        verbose_name_plural = 'To Do List'

    def __str__(self):

        return self.user.username + self.item[:20]
