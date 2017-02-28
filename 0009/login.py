#coding:utf-8

import urllib.request
import urllib.parse
import http.cookiejar
import json

cj = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)

url = "https://passport.weibo.cn/sso/login"

postdata = {
    "username":"username",
    "password":"password",
    "savestate":"1",
    "r":"http://m.weibo.cn/",
    "ec":"0",
    "pagerefer":"https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F",
    "entry":"mweibo",
    "wentry":"",
    "loginfrom":"",
    "client_id":"",
    "code":"",
    "qq":"",
    "mainpageflag":"1",
    "hff":"",
    "hfp":"",
}

headers = {
    "Accept":"application/json, text/plain, */*",
    #"Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-US,en;q=0.8",
    "Connection":"keep-alive",
#    "Content-Length":"288",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"_T_WM=629886d58ed30fd4036432e275322a29",
    "Host":"passport.weibo.cn",
    "Origin":"https://passport.weibo.cn",
    "Referer":"https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/57.0.2987.74 Safari/537.36",
}

request = urllib.request.Request(
    url,
    urllib.parse.urlencode(postdata).encode(),
    headers,
)

response = urllib.request.urlopen(request)

if json.loads(response.read().decode())['retcode'] == 20000000:
    print('登录成功')
else:
    print('登录失败')


cookies = [c.name + "=" + c.value for c in cj]
cookies.append(headers['Cookie'])
headers['Cookie'] = ";".join(cookies)
#print(headers['Cookie'])
headers["Host"] = "m.weibo.cn"

url = "http://m.weibo.cn/container/getIndex?uid=1643971635&luicode=20000174&type=uid&value=1643971635&containerid=1076031643971635&page=1"
request = urllib.request.Request(
    url,
    None,
    headers,
)
response = urllib.request.urlopen(request)
print(json.loads(response.read().decode()))
