#coding:utf-8

import os
import re
import datetime
import urllib.request
import urllib.parse
import webbrowser
import random
import threading
import queue
import time
from user_agent import agents
from http.cookiejar import CookieJar

# 0-存储经纬度 1-存储地理位置
LOCATION = 0

# 线程数
THREADS = 7

root_url = "http://122.224.8.156:7288/"
login_url = root_url + "Default.aspx"
check_code_url = root_url + "ValidateCode.aspx"

# 车辆详情
vehicle_detail_url = root_url + "HomePage/AllVehicleInfoDetails.aspx?holdID=10046&stateID=0&times=7-4"

# 车辆行驶记录
trace_detail_url = root_url + "ReportPage/VehicleTravelDetail.aspx?objID={}&time={}"

# 位置信息
location_url = "http://220.178.1.19:7269/GetAddr.aspx?lon={}&lat={}&type={}"

# 构造带cookie的opener
cj = CookieJar()
handler = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)
cookie = None

# 暂存车辆详情
vehicle_details = []

# 错误日志
error_log = []

# 返回utf-8解码后的response
decoded_resp = lambda req: send_response(req).read().decode('utf-8')

# 返回byte类的response
byte_resp = lambda req: send_response(req).read()


def send_response(request):
    """超时二次请求"""
    try:
        return urllib.request.urlopen(request, timeout=5)
    except:
        try:
            return urllib.request.urlopen(request, timeout=10)
        except Exception as e:
            print(e)
        return None


def get_viewstate(html):
    """return string viewstate"""

    viewstate = re.findall(r'''id="__VIEWSTATE" value="(.*?)"''', html)
    #print(viewstate)
    return viewstate[0]


def get_check_code():
    """return check code and set cookie"""

    global cookie

    # check code
    chk_dir = os.path.dirname(os.path.abspath(__file__)) + '/CheckCode.aspx'
    print('check code path:', chk_dir)
    response = byte_resp(check_code_url)
    with open(chk_dir, 'wb') as f:
        f.write(response)
    webbrowser.open(chk_dir)

    # cookie
    for c in cj:
        cookie = c.name + "=" + c.value
    #print(cookie)
    return input("输入验证码:")


def get_headers():
    """headers"""

    headers = {
        "Host": "122.224.8.156:7288",
        "User-Agent": random.choice(agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        #"Accept-Encoding": "gzip, deflate",
        "Cookie": cookie,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0, no-cache",
        "Origin": "http://122.224.8.156:7288",
        "Referer": "http://122.224.8.156:7288/Default.aspx",
    }
    #print(headers['User-Agent'])
    return headers


def get_login_post_data():
    """return bytes of urlencoded post data"""

    post_data = {
        "__EVENTTARGET": "btnLogin",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": get_viewstate(decoded_resp(login_url)),
        "txtUserName": "xxxxxxx",
        "txtPassword": "xxxxxxx",
        "txtValidateCode": get_check_code(),
        "hidpsd": "qaz123ZX",
    }
    #print(post_data)
    return urllib.parse.urlencode(post_data).encode()


def login():
    """login"""

    request = urllib.request.Request(
        login_url,
        get_login_post_data(),
        get_headers(),
    )
    response = decoded_resp(request)
    if '验证码不正确' in response:
        print("验证码不正确")
        login()
    elif '用户密码不正确' in response:
        print("用户密码不正确")
        login()
    else:
        print("登录成功")


def get_vehicle_detail_post_data():
    """return bytes of urlencoded post data"""

    # 获取车辆详情页面的viewstate
    request = urllib.request.Request(
        vehicle_detail_url,
        None,
        get_headers(),
    )
    __VIEWSTATE = get_viewstate(decoded_resp(request))

    # 请求每页显示200条数据
    post_data = {
        "__EVENTTARGET": "ddlCount",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": __VIEWSTATE,
        "ddlGoPage": "1",
        "ddlCount": "200",
        "txtTimeID": "",
        "txtHoldID": "10046",
        "txtStateID": "0",
        "txtIsStop": "",
    }
    request = urllib.request.Request(
        vehicle_detail_url,
        urllib.parse.urlencode(post_data).encode(),
        get_headers(),
    )
    response = decoded_resp(request)
    index, page = re.findall(r'共有.*?>(\d+)<.*?>\d+/(\d+)<', response)[0]
    print("共有{}辆车, {}页.".format(index, page))

    # 如果只有一页就直接返回response, 否则返回每页的post data
    if page == '1':
        yield response
    else:
        print("获取第1页")
        yield urllib.parse.urlencode(post_data).encode()
        for i in range(1, int(page)):
            post_data['__EVENTTARGET'] = "btnNext"
            post_data['ddlGoPage'] = str(i)
            post_data['__VIEWSTATE'] = get_viewstate(response)
            print("获取第{}页".format(i+1))
            yield urllib.parse.urlencode(post_data).encode()


def get_vehicle_detail():
    """save vehicle detail into vehicle_details"""

    global vehicle_details

    for post_data in get_vehicle_detail_post_data():

        # 判断返回来的是post data还是response
        if not isinstance(post_data, str):
            request = urllib.request.Request(
                vehicle_detail_url,
                post_data,
                get_headers(),
            )
            response = decoded_resp(request)
        else:
            response = post_data

        # 暂存车辆详情(主要为了后面遍历车辆用)
        detail = re.findall(r'<td>(.*?)</td>'*8, response)
        vehicle_details += detail
    print(" * 确认计数：", len(set(vehicle_details)))
    with open('details.txt', 'w+') as f:
        for i in vehicle_details:
            f.write(str(i) + '\n')
    #print(vehicle_details)


def get_vehicle_trace_post_data(vid, date):
    """return post data"""

    # get viestate
    request = urllib.request.Request(
        trace_detail_url.format(vid, date),
        None,
        get_headers(),
    )
    __VIEWSTATE = get_viewstate(decoded_resp(request))

    # 请求200条数据每页
    post_data = {
        "__EVENTTARGET": "ddlCount",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": __VIEWSTATE,
        "ddlGoPage": "1",
        "ddlCount": "200",
        "txtFunID": "",
        "txtMaxCount": "",
        "hidCameraCount": "",
        "hidObjctID": vid,
    }
    request = urllib.request.Request(
        trace_detail_url.format(vid, date),
        urllib.parse.urlencode(post_data).encode(),
        get_headers(),
    )
    response = decoded_resp(request)
    index, page = re.findall(r'共有.*?>(\d+)<.*?>\d+/(\d+)<', response)[0]
    print("[{}]: {} {} 共有{}条记录, {}页.".format(
        threading.current_thread().getName(), vid, date, index, page))

    # 和上面一样根据页数返回对应的数据
    if page == '1':
        yield response
    else:
        print("获取第1页")
        yield urllib.parse.urlencode(post_data).encode()
        for i in range(1, int(page)):
            post_data['__EVENTTARGET'] = "btnNext"
            post_data['ddlGoPage'] = str(i)
            post_data['__VIEWSTATE'] = get_viewstate(response)
            print("获取第{}页".format(i+1))
            yield urllib.parse.urlencode(post_data).encode()


def get_daily_data_and_formatter(mode=0):
    """select title and formatter"""

    daily_data = [('车辆编号', '车牌号码', '车牌颜色', '所属企业',
                   '车辆状态', '开始时间', '经度', '纬度', '类型',
                   '结束时间', '持续时间')]

    daily_data_l = [('车辆编号', '车牌号码', '车牌颜色',
                     '所属企业', '车辆状态', '开始时间',
                     '开始位置', '结束时间', '持续时间')]

    formatter = (
        "{0[1]}, {0[3]}, {0[4]}, {0[5]}, "
        "'{0[6]} {0[7]} {0[8]}', {0[9]}, {0[10]}\n"
    )

    formatter_l = (
        "{0[1]}, {0[3]}, {0[4]}, {0[5]}, "
        "'{0[6]}', {0[7]}, {0[8]}\n"
    )
    return ([daily_data, daily_data_l][mode], [formatter, formatter_l][mode])


def get_vehicle_trace_detail(q):
    """save vehicle trace into files"""

    today = datetime.date.today()

    while not q.empty():
        i = q.get()
        # 过去一周的第一天
        date = (today-datetime.timedelta(days=8-i)).strftime('%Y-%m-%d')

        # 按天遍历每辆车
        for vehicle in vehicle_details:
            try:
                daily_data, formatter = get_daily_data_and_formatter(LOCATION)

                # 遍历每辆车一天中的所有记录
                for post_data in get_vehicle_trace_post_data(vehicle[0], date):
                    if not isinstance(post_data, str):
                        request = urllib.request.Request(
                            trace_detail_url.format(vehicle[0], date),
                            post_data,
                            get_headers(),
                        )
                        response = decoded_resp(request)
                    else:
                        response = post_data
                    p1 = r"textCenter.*?" + r"<td>(.*?)</td>"*6
                    p2 = r".*?&quot;(.*?)&quot;,&quot;(.*?)&quot;,(.*?),&quot;.*?&quot;"
                    p3 = r".*?<td>(.*?)</td><td>(.*?)</td>"
                    detail = re.findall(p1+p2+p3, response, re.S)

                    # 选择经纬度或者位置存储
                    if LOCATION == 1:
                        newdetail = []
                        for d in detail:
                            request = urllib.request.Request(
                                location_url.format(d[6], d[7], d[8]),
                                None,
                                get_headers(),
                            )
                            content = byte_resp(request).decode('gbk')
                            location = re.findall(r"<msg>(.*?)</msg>", content)[0]
                            newdetail.append(d[:6] + (location, ) + d[9:])
                        temp = newdetail
                    else:
                        temp = detail
                    daily_data += temp
                print(" * 确认计数：{} {} {}条".format(
                    vehicle[0], date, len(set(daily_data))-1))
            except Exception as e:
                print(e)
                error = " * {} {}数据获取失败".format(vehicle[0], date)
                print(error)
                error_log.append(error)
                continue
            if not os.path.isdir(os.path.join(vehicle[3], vehicle[0])):
                os.makedirs(os.path.join(vehicle[3], vehicle[0]))
            with open(os.path.join(vehicle[3], vehicle[0], date+'.txt'),
                'w+', encoding='utf-8') as f:
                for item in daily_data:
                   f.write(formatter.format(item))


def multithread_running():
    q = queue.Queue()
    for day in range(1, 8):
        q.put(day)

    start = time.time()
    threads = []
    for i in range(THREADS):
        t = threading.Thread(
            target=get_vehicle_trace_detail,
            args=(q,)
        )
        t.daemon = True
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    print("耗时  {}s".format(time.time()-start))
    if error_log:
        print('-'*20)
        with open('error.log', 'w+') as f:
            for e in error_log:
                print(e)
                f.write(e + '\n')
        print('-'*20)

if __name__ == '__main__':

    login()
    get_vehicle_detail()
    multithread_running()
