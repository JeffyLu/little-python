#-*- coding:utf-8 -*-

import re
import os
from struct import pack, unpack
import datetime

class Operate():
    """日志操作类"""

    _filename = ''
    _count = 0
    _logs = []

    #载入日志
    def __init__(self, filename):
        self._filename = filename
        self._load()

    def _pack_byte(self, log):
        """字节流打包"""

        btype = pack('i', log['type'])
        buser = pack('i', log['user']['length'])
        buser += log['user']['user'].encode('gbk')
        bdate = pack('i', log['date']['length'])
        bdate += log['date']['date'].encode('gbk')
        btext = pack('i', log['text']['length'])
        btext += log['text']['text'].encode('gbk')
        return btype + buser + bdate + btext

    def _unpack_byte(self, t, f, length = 0):
        """字节流解包"""

        #4个字节解析为int型整数
        if t == 'int':
            return unpack('i', f.read(4))[0]

        #length长度字符串解码('gbk')
        elif t == 'string':
            return unpack('%ds' % length, f.read(length))[0].decode('gbk')
        else:
            return None

    def _load(self):
        """载入日志"""

        with open(self._filename, 'rb') as f:

            #读取记录总数
            self._count = self._unpack_byte('int', f)

            #按格式解析并保存所有记录
            for i in range(self._count):

                #单条记录格式
                log = {'type':'', 'user':{}, 'date':{}, 'text':{}}
                #类型
                log['type'] = self._unpack_byte('int', f)
                #用户名以及长度
                log['user']['length'] = self._unpack_byte('int', f)
                log['user']['user'] = self._unpack_byte(
                    'string',
                    f,
                    log['user']['length']
                )
                #日期以及长度
                log['date']['length'] = self._unpack_byte('int', f)
                log['date']['date'] = self._unpack_byte(
                    'string',
                    f,
                    log['date']['length']
                )
                #内容信息以及长度
                log['text']['length'] = self._unpack_byte('int', f)
                log['text']['text'] = self._unpack_byte(
                    'string',
                    f,
                    log['text']['length']
                )
                self._logs.append(log)

    def _input_index(self, string, mflag = False):
        """输入区间"""

        index = str(input(string))
        while(not re.match(r'[1-9]+\d* [1-9]+\d*', index)):
            index = input('输入无效, 请重新输入:')
        index = list(map(int, index.split(' ')))

        #移动操作左右区间不排序
        if mflag:
            return index

        #左右区间排序
        index.sort()
        l = index[0] if index[0] <= self._count else self._count
        r = index[1] if index[1] <= self._count else self._count
        return l, r

    def _get_log(self, index):
        """按下标取出记录"""

        log = self._logs[index]
        #格式化
        format_log = str.format("%d %s%s %s" % (
            log['type'],
            log['user']['user'],
            log['date']['date'],
            log['text']['text'],
        ))
        return format_log

    def read(self):
        """读取日志"""

        print('共有%d条记录.' % self._count)
        l, r = self._input_index('输入查询区间, 如:10 20\n')
        print('查询区间为%d-%d.' % (l, r))
        for i in range(l-1, r):
            print(i+1, self._get_log(i))

    def delete(self):
        """删除日志"""

        l, r = self._input_index('输入删除区间, 如:10 20\n')
        confirm = input('是否删除记录%d-%d\n确认(y),任意键取消.\n' % (l, r))
        if confirm != 'y':
            print('已放弃删除!')
            return

        for i in range(r-l+1):
            print('成功删除:', l+i, self._get_log(l-1))
            self._logs.pop(l-1)
            self._count -= 1

        self._save()

    def add(self):
        """添加日志"""

        log = {'type':'', 'user':{}, 'date':{}, 'text':{}}

        #输入新记录
        while(True):
            try:
                log['type'] = int(input('输入记录类型:'))
                break
            except:
                print('输入无效, 请输入一个整数!')

        log['user']['user'] = input('输入用户名:')
        log['date']['date'] = datetime.datetime.now().strftime(' %Y-%m-%d, %H:%M')
        log['text']['text'] = input('输入记录信息:')

        #计算长度
        log['user']['length'] = len(log['user']['user'].encode('gbk'))
        log['date']['length'] = len(log['date']['date'].encode('gbk'))
        log['text']['length'] = len(log['text']['text'].encode('gbk'))

        #添加并保存
        self._logs.append(log)
        self._count += 1
        print('成功添加:', self._count, self._get_log(self._count-1))
        self._save()

    def change(self):
        """修改日志"""

        #取出带修改记录
        while True:
            try:
                index = int(input('输入待修改记录序号, 如:10\n'))
                if index < 1 or index > self._count:
                    raise
                break
            except:
                print('输入无效, 请输入1-%d内的整数!' % self._count)
        print('待修改的记录:', index, self._get_log(index-1))
        log = self._logs[index-1]

        #输入修改数据
        while True:
            temp_type = input('输入新类型(回车跳过):')
            try:
                if temp_type:
                    temp_type = int(temp_type)
                else:
                    temp_type = log['type']
                break
            except:
                print('输入无效, 请输入一个整数!')
        temp_user = input('输入新用户(回车跳过):')
        if not temp_user:
            temp_user = log['user']['user']
        temp_date = datetime.datetime.now().strftime(' %Y-%m-%d, %H:%M')
        temp_text = input('输入新记录信息(回车跳过):')
        if not temp_text:
            temp_text = log['text']['text']

        #修改并保存
        print('修改后的记录: %d %d %s%s %s' % (
            index, temp_type, temp_user, temp_date, temp_text))
        confirm = input('是否修改该记录?\n确认(y),任意键取消.\n')
        if confirm != 'y':
            print('已取消修改!')
            return

        log['type'] = temp_type
        log['user']['user'] = temp_user
        log['user']['length'] = len(temp_user.encode('gbk'))
        log['date']['date'] = temp_date
        log['date']['length'] = len(temp_date.encode('gbk'))
        log['text']['text'] = temp_text
        log['text']['length'] = len(temp_text.encode('gbk'))
        self._logs[index-1] = log
        print('修改成功!')
        self._save()

    def move(self):
        """移动日志"""

        current_position, target_position = self._input_index(
            '输入待移动日志位置和目标位置, 如:10 20\n',
            mflag = True
        )

        #移动并保存
        print('成功移动\n%d %s' % (
            current_position, self._get_log(current_position-1)))
        log = self._logs.pop(current_position-1)
        self._logs.insert(target_position-1, log)
        print('至\n%d %s' % (
            target_position, self._get_log(target_position-1)))
        self._save()

    def _save(self):
        """保存文件"""

        with open('chrom2000.log', 'wb') as f:
            f.write(pack('i', self._count))
            for log in self._logs:
                f.write(self._pack_byte(log))

def main():
    """操作日志文件

    选项：
          a --> 添加日志
          c --> 修改日志
          d --> 删除日志
          m --> 移动日志
          r --> 读取日志
          q --> 退出

    学号:105032014029    姓名:卢键辉
    """

    #创建对象
    FILE_NAME = 'chrom2000.log'
    log = Operate(FILE_NAME)

    #主程序
    while(True):
        choice = input('输入选项:')
        if choice == 'r':
            log.read()

        elif choice == 'd':
            log.delete()

        elif choice == 'a':
            log.add()

        elif choice == 'c':
            log.change()

        elif choice == 'm':
            log.move()

        elif choice == 'q':
            print('goodbye!')
            break

        else:
            print('输入无效!')

if __name__ == '__main__':

    print(main.__doc__)
    main()
