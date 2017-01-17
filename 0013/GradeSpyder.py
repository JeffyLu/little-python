#coding:utf-8

import urllib.request
import urllib.parse
import re
import http.cookiejar

#url
url = "http://jwgl.xxxx.edu.cn/"
login_url = url + "default2.aspx"
chkcode_url = url + "CheckCode.aspx"
grade_url = url + "xscjcx_dq.aspx?"

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

        response = urllib.request.urlopen(chkcode_url)
        with open('CheckCode.aspx', 'wb') as f:
            f.write(response.read())
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
            'gnmkdm' : 'N121617',
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
            'ddlxn' : input('输入学年, 如(2016-2017):'),
            'ddlxq' : input('输入学期, 如(1):'),
            'btnCx' : ' 查  询 ',
        }

        return (urllib.parse.urlencode(data).encode(), url)

    @property
    def __get_headers(self):

        headers = {
            "Accept" :
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent" :
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/53.0.2785.116 Safari/537.36",
            "Referer" : "http://jwgl.xxxx.edu.cn/xs_main.aspx?xh=" + self.__stuid,
            "Connection" : "keep-alive",
            "Cookie" : self.__cookie,
            "Host" : "jwgl.xxxx.edu.cn",
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

        content = content.replace('&nbsp;', '-')
        title = re.findall(r'<td colspan="3".*>(.*?)</td>', content)
        department = re.findall(r'<td>(学院.*?)</td>', content)
        _class = re.findall(r'<td>(行政班.*?)</td>', content)
        major = re.findall(r'<td colspan="2">(专业.*?)</td>', content)
        grade_pattern = '<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>'
        grade = re.findall(grade_pattern, content)
        print(department[0])
        print(_class[0])
        print('学号:'+self.__stuid)
        print('姓名:'+self.__name)
        print('\n' + '*-'*20 + title[0] + '-*'*20 + '\n')
        for l in grade:
            print('%-22s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s' %
                  (l[3][:9], l[6], l[7], l[8], l[9], l[10])
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
