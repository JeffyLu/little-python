#coding:utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ip, Info
from .forms import BMIForm
import pylab as pl
import numpy as np

#配置中文字体
import matplotlib as mpl
zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/wps-office/FZFSK.TTF')

# Create your views here.

#获取ip地址
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


#BMI计算视图
def view_of_BMI(request):
    ip = get_ip(request)
    if request.method == 'POST':
        form = BMIForm(request.POST)

        #非法用户
        try:
            if Ip.objects.get(ip = ip).blackone:
                return HttpResponse('非法用户:' + ip)
        except:
            Ip.objects.create(ip = ip)

        #提交表单获取干净数据
        if form.is_valid():
            Info.objects.create(
                ip = Ip(ip),
                age = form.clean_age(),
                gender = form.cleaned_data['gender'],
                height = form.clean_height(),
                weight = form.clean_weight(),
            )
            return HttpResponseRedirect('/bmi')

    else:
        form = BMIForm()

    #显示最近5条数据
    try:
        history_data = Info.objects.filter(ip = ip)
        history_data = history_data.order_by('-date')[:5]
    except:
        history_data = None
    context = {
        'form' : form,
        'ip' : ip,
        'history_data' : history_data,
    }
    return render(request, 'BMI.html', context)


#个人数据统计
def stat_personal(ip):
    filename = './commonstatic/statistics/my.jpg'

    #统计记录个数
    try:
        ip = Ip.objects.get(ip = ip)
        items = ip.info_set.count()
    except:
        return 0

    #提取数据
    my_info = Info.objects.filter(ip = ip).order_by('date')
    dates = list(range(len(my_info)))
    bmis = []
    for info in my_info:
        bmis.append(info.get_bmi())

    #构造图表
    pl.figure('my', figsize = (5.2, 2.8), dpi = 100)
    pl.plot(dates, bmis, '*-', color = '#20b2aa', linewidth = 1.5)
    pl.ylabel(u'BMI值', fontproperties = zhfont)
    pl.ylim(0.0, 50.0)
    pl.savefig(filename)
    pl.cla()
    return items


#各年龄段BMI平均值
def stat_all_by_age():
    filename = './commonstatic/statistics/all0.jpg'

    #提取数据
    bmi_by_age = []
    sum_of_bmi = 0
    count = 0
    #提取各年龄段bmi和数与记录数量
    for i in range(1, 151):
        infos = Info.objects.filter(age = i)
        count += len(infos)
        if infos:
            for info in infos:
                sum_of_bmi += info.get_bmi()
        else:
            sum_of_bmi += 0
        if not i%10:
            bmi_by_age.append((i, sum_of_bmi, count))
            sum_of_bmi = 0
            count = 0
    ages = [i for i in range(10, 151, 10)]
    avebmi = [0 if i[1] == 0 else round(i[1]/i[2], 1) for i in bmi_by_age]

    #构造图表
    pl.figure('all0', figsize = (5.2, 2.8), dpi = 100)
    pl.xlabel(u'年龄段', fontproperties = zhfont)
    pl.ylabel('平均BMI', fontproperties = zhfont)
    pl.ylim(0.0, 50.0)
    pl.plot(ages, avebmi, '*', color = '#20b2aa')
    pl.savefig(filename)
    pl.cla()

    avecount = [i[2] for i in bmi_by_age]
    ages = ['%d-%d'%(i-9, i) for i in ages]
    return list(zip(ages, avebmi, avecount))


#健康等级分布情况
def stat_all_by_rank():
    filename = './commonstatic/statistics/all1.jpg'
    #pl.figure('all1', figsize = (5.2, 2.8), dpi = 100)

    #提取数据
    ranks = ['偏瘦', '正常', '偏胖', '肥胖', '重度肥胖', '极度肥胖']
    men_infos = Info.objects.filter(gender = '男')
    women_infos = Info.objects.filter(gender = '女')
    men_ranks = [i.get_rank() for i in men_infos]
    women_ranks = [i.get_rank() for i in women_infos]
    men_count = [men_ranks.count(r) for r in ranks]
    women_count = [women_ranks.count(r) for r in ranks]

    #构造图表
    ind = np.arange(6)
    width = 0.35
    fig, ax = pl.subplots(figsize = (5.2, 2.8))
    rects1 = ax.bar(ind, men_count, width, color = '#20b2aa')
    rects2 = ax.bar(ind + width, women_count, width, color = 'w')
    ax.set_ylabel('数量', fontproperties = zhfont)
    ax.set_xlim(-0.5, 7)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(ranks, fontproperties = zhfont)
    ax.legend((rects1[0], rects2[0]), ('Men', 'Women'), fontsize = 'small')
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(
                rect.get_x() + rect.get_width() / 2,
                1.05 * height,
                '%d' % int(height),
                ha = 'center',
                va='bottom',
            )
    autolabel(rects1)
    autolabel(rects2)
    fig.savefig(filename)
    fig.clear()


#站点数据视图
def view_of_stat(request):
    #获取数据信息
    ip = get_ip(request)
    ip_count = Ip.objects.count()
    items_count = Info.objects.count()

    #获取三个图表
    items = stat_personal(ip)
    age_bmi_count = stat_all_by_age()
    stat_all_by_rank()

    context = {
        'ip' : ip,
        'items' : items,
        'ip_count' : ip_count,
        'items_count' : items_count,
        'age_bmi_count' : age_bmi_count,
    }

    return render(request, 'statistics.html', context)


#健康之家视图
def view_of_health_home(request):
    return render(request, 'health_home.html')
