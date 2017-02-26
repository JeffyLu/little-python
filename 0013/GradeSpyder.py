#coding:utf-8

import urllib.request
import urllib.parse
import re
import webbrowser
import http.cookiejar
import os

#url
url = "http://jwgl.fjnu.edu.cn/"
login_url = url + "default2.aspx"
chkcode_url = url + "CheckCode.aspx"
grade_url = url + "xscjcx.aspx?"

#cookie
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
        #print(viewstate)
        return viewstate[0]

    @property
    def __get_check_code(self):

        chk_dir = os.path.dirname(os.path.abspath(__file__)) + '/CheckCode.aspx'
        print('check code path:', chk_dir)
        response = urllib.request.urlopen(chkcode_url)
        with open(chk_dir, 'wb') as f:
            f.write(response.read())
        webbrowser.open(chk_dir)
        check_code = input("输入验证码:")
        for c in cj:
            self.__cookie = c.name + "=" + c.value
        #print(self.__cookie)
        return check_code

    @property
    def __get_login_post_data(self):

        response = urllib.request.urlopen(login_url)
        content = response.read().decode('gbk')
        viewstate = self.__get_viewstate(content)
        self.__stuid = input('输入学号:')
        self.__password = input('输入密码:')
        if not self.__stuid:
            self.__stuid = '105032014029'
            self.__password = '214121.a'
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
    def __get_grade_post_data_and_url(self):

        data = {
            'xh' : self.__stuid,
            'xm' : self.__name,
            'gnmkdm' : 'N121618',
        }
        url = grade_url + urllib.parse.urlencode(data)

        request = urllib.request.Request(
            url,
            None,
            self.__get_headers,
        )
        response = urllib.request.urlopen(request)
        content = response.read().decode('gbk')
        #print(url)

        data = {
            '__EVENTTARGET' : '',
            '__EVENTARGUMENT' : '',
            '__VIEWSTATE' : self.__get_viewstate(content),
            'ddlXN' : input('输入学年, 如(2016-2017):'),
            'ddlXQ' : input('输入学期, 如(1):'),
            'ddl_kcxz' : '',
            'btn_xq' : '学期成绩',
        }

        return (urllib.parse.urlencode(data).encode(), url)

    @property
    def __get_headers(self):

        headers = {
            "Accept" :
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent" :
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/53.0.2785.116 Safari/537.36",
            "Referer" : "http://jwgl.fjnu.edu.cn/xs_main.aspx?xh=" + self.__stuid,
            "Connection" : "keep-alive",
            "Cookie" : self.__cookie,
            "Host" : "jwgl.fjnu.edu.cn",
        }

        return headers

    def login(self):

        try:
            request = urllib.request.Request(
                login_url,
                self.__get_login_post_data,
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
            return True
        else:
            print('登录失败!')

        return False

    def get_grade(self):

        data, url = self.__get_grade_post_data_and_url
        #print(data, url, self.__get_headers)
        try:
            request = urllib.request.Request(
                url,
                data,
                self.__get_headers,
            )
            response = urllib.request.urlopen(request)
            content = response.read().decode('gbk')
            self.__analyze_info(content)
        except urllib.request.HTTPError:
            print('http error!')
            return False


    def __analyze_info(self, content):

        #print(content)
        content = content.replace('&nbsp;', '-')
        content = re.sub('<a .*?>(?P<t>.*?)</a>', lambda c: c.group('t'), content)
        title = re.findall(r'"lbl_bt">.*>(.*?)</font>', content)
        department = re.findall(r'"lbl_xy">(学院.*?)</span>', content)
        _class = re.findall(r'"lbl_xzb">(.*?)</span>', content)
        major = re.findall(r'"lbl_zyfx">(专业.*?)</span>', content)
        grade_pattern = '<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>'
        grade = re.findall(grade_pattern, content)
        print(department[0])
        print(_class[0])
        print('学号:'+self.__stuid)
        print('姓名:'+self.__name)
        print('\n' + '*-'*20 + title[0] + '-*'*20 + '\n')
        for l in grade:
            print('%-22s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s' %
                  (l[3][:9], l[6], l[7].strip(), l[8], l[10], l[11])
                 )
        o = input('\n*输入“f”查看完整信息:\n')
        if o == 'f':
            for l in grade:
                for i in l:
                    print(i + ' ', end='')
                print()

if __name__ == '__main__':

    op = GradeSpyder()
    while True:
        if op.login():
            break
        else:
            print('重新登录!')
    op.get_grade()
