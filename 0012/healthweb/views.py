from django.shortcuts import render
from django.http import HttpResponse
from BMI.models import Ip, Info
from django.db import transaction
import random

#主页视图
def index(request):
    return render(request, 'index.html')

#随机添加数据
@transaction.atomic
def add_items(request):

    gender_choice = ['男', '女']
    html = []

    #记录个数
    for i in range(100):
    #for i in range(1000):

        ip = ".".join([str(random.randint(1, 254)) for i in range(4)])
        age = random.randint(10, 70)
        gender = random.choice(gender_choice)
        height_choice = {
            '男' : round(random.uniform(150, 190), 1),
            '女' : round(random.uniform(140, 180), 1),
        }
        weight_choice = {
            '男' : round(random.uniform(150, 190), 1),
            '女' : round(random.uniform(140, 180), 1),
        }
        height = height_choice[gender]
        weight = weight_choice[gender]
        bmi = weight/2 / (height/100 * height/100)
        #排除无用数据
        if bmi > 40 or bmi < 18.5:
            continue
        Ip.objects.create(ip = ip)
        Info.objects.create(
            ip = Ip(ip),
            age = age,
            gender = gender,
            height = height,
            weight = weight,
        )
        #输出结果
        result = "<tr><td>%s</td><td>%d</td><td>%s</td><td>%.1f</td>\
                <td>%.1f</td><td>%.4f</td></tr>" % (
            ip, age, gender, height, weight, bmi)
        html.append(result)
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

