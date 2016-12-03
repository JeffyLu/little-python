from django.contrib import admin
from mylist.models import *
# Register your models here.

class MylistAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'item',
        'status',
    ]

admin.site.register(Mylist, MylistAdmin)
