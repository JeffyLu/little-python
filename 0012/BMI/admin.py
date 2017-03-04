from django.contrib import admin
from BMI.models import Ip, Info
# Register your models here.

#显示外键
class InfoInline(admin.StackedInline):
    model = Info
    extra = 0

#ip管理
class IpAdmin(admin.ModelAdmin):
    #搜索框
    search_fields = ['ip',  ]
    #过滤栏
    list_filter = ['blackone', ]
    #显示列表
    list_display = [
        'ip',
        'latestvisit',
        'blackone',
        'remark',
    ]
    #显示外键
    inlines = [InfoInline]

#信息管理
class InfoAdmin(admin.ModelAdmin):
    lists = [
        'ip',
        'get_bmi',
        'get_rank',
        'age',
        'gender',
        'height',
        'weight',
        'date',
    ]

    list_filter = ['gender', ]
    list_display = lists
    search_fields = ['ip__ip', ]

#注册
admin.site.register(Ip, IpAdmin)
admin.site.register(Info, InfoAdmin)
