#coding:utf-8

import urllib.request
import urllib.parse
import re
import http.cookiejar

url = "http://jwgl.xxxx.edu.cn/"
login_url = url + "default2.aspx"
chkcode_url = url + "CheckCode.aspx"
grade_url = url + "xscjcx_dq.aspx?"

cj = http.cookiejar.CookieJar()
pro = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(pro)
urllib.request.install_opener(opener)

class GradeSpyder:

    def __init__(self):

        self.__cookie = None
        self.__name = None
        self.__stuid = None
        self.__password = None

    def __get_viewstate(self, content):

        viewstate = re.findall(r'''name="__VIEWSTATE" value="(.*?)"''', content)
        print(viewstate)
        return viewstate[0]

    @property
    def __get_check_code(self):

        response = urllib.request.urlopen(chkcode_url)
        with open('CheckCode.aspx', 'wb') as f:
            f.write(response.read())
        check_code = input("输入验证码:")
        for c in cj:
            self.__cookie = c.name + "=" + c.value
        print(self.__cookie)
        return check_code

    @property
    def __get_post_data(self):

        response = urllib.request.urlopen(login_url)
        content = response.read().decode('gbk')
        viewstate = self.__get_viewstate(content)
        self.__stuid = input('输入学号:')
        self.__password = input('输入密码:')
        check_code = self.__get_check_code
        identity = "学生"

        post_data = {
            'txtUserName' : self.__stuid,
            'TextBox2' : self.__password,
            'txtSecretCode' : check_code,
            'RadioButtonList1' : identity,
            '__VIEWSTATE' : viewstate,
            'Button1' : '',
            'lbLanguage' : '',
            'hidPdrs' : '',
            'hidsc' : '',
        }

        return urllib.parse.urlencode(post_data).encode()

    @property
    def __get_headers(self):

        headers = {
            "Accept" :
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent" :
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/53.0.2785.116 Safari/537.36",
            "Referer " : "http://jwgl.fjnu.edu.cn/xs_main.aspx?xh=" + self.__stuid,
            "Connection" : "keep-alive",
            "Cookie" : self.__cookie,
            "Host" : "jwgl.fjnu.edu.cn",
        }

        return headers

    def login(self):

        try:
            request = urllib.request.Request(
                login_url,
                self.__get_post_data,
                self.__get_headers,
            )
            response = urllib.request.urlopen(request)
            content = response.read().decode('gbk')
        except urllib.request.HTTPError:
            print('http error!')
            return False

        if '验证码不正确！！' in content:
            print('验证码不正确!')
        elif '密码错误！！' in content:
            print('帐号或密码错误!')
        elif '欢迎您：' in content:
            name = re.findall(r'''<span id="xhxm">(.*?)同学''', content)
            self.__name = name[0]
            print('登录成功!')
            print('欢迎{}, {}同学:'.format(self.__stuid, self.__name))
            return True
        else:
            print('登录失败!')

        return False

    def get_grade(self):
        pass

if __name__ == '__main__':

    op = GradeSpyder()
    while True:
        if op.login():
            break
        else:
            print('重新登录!')
    op.get_grade()
