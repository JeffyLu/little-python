from django.db import models

# Create your models here.

#ip表
class Ip(models.Model):
    ip = models.GenericIPAddressField(
        'IP',
        primary_key = True,
    )

    blackone = models.BooleanField(
        '黑名单',
        default = False,
    )

    latestvisit = models.DateTimeField(
        '最近访问',
        auto_now_add = True,
    )

    remark = models.TextField(
        '备注',
        max_length = 100,
        blank = True,
        null = True,
    )

    class Meta:
        #后台显示名称
        verbose_name_plural = 'IP管理'

    def __str__(self):
        return self.ip

#信息表
class Info(models.Model):
    ip = models.ForeignKey(
        Ip,
        verbose_name = 'IP',
        on_delete = models.CASCADE,
    )

    age = models.IntegerField(
        '年龄',
    )

    GENDER_CHOICE = (('男', '男'), ('女', '女'))
    gender = models.CharField(
        '性别',
        max_length = 1,
        choices = GENDER_CHOICE,
    )

    height = models.DecimalField(
        '身高',
        max_digits=4,
        decimal_places=1,
    )

    weight = models.DecimalField(
        '体重',
        max_digits=4,
        decimal_places=1,
    )

    date = models.DateTimeField(
        '填写日期',
        auto_now_add = True,
    )

    #获取BMI
    def get_bmi(self):
        bmi = (self.weight/2) / (self.height/100 * self.height/100)
        return round(bmi, 1)
    get_bmi.short_description = 'BMI'
    get_bmi.admin_order_field = 'ip__ip'

    #获取等级
    def get_rank(self):
        bmi = self.get_bmi()
        if bmi < 18.5:
            return "偏瘦"
        elif bmi >= 18.5 and bmi <= 24.9:
            return "正常"
        elif bmi >= 25.0 and bmi <= 29.9:
            return "偏胖"
        elif bmi >= 30.0 and bmi <= 34.9:
            return "肥胖"
        elif bmi >= 35.0 and bmi <= 39.9:
            return "重度肥胖"
        else:
            return "极度肥胖"
    get_rank.short_description = '等级'
    get_rank.admin_order_field = 'ip__ip'

    class Meta:
        #后台显示名称
        verbose_name_plural = '参数管理'
        verbose_name = 'BMI指数'

    def __str__(self):
        return str(self.get_bmi())

