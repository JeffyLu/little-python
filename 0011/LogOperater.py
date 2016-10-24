#-*- coding:utf-8 -*-

import re
import os
from struct import pack, unpack
import datetime

class Operate():
    """日志操作"""

    __count = 0
    #构造函数
    def __init__(self, filename):
        self.__filename = filename
        with open(self.__filename, 'rb') as f:

            #读取4个字节为日志数目
            self.__count = unpack('i', f.read(4))[0]

    #读取日志
    def read(self):
        print('共有%d条日志.' % self.__count)
        l, r = self.__input_index('输入查询区间, 如:10 20\n')
        print('查询区间为%d-%d.' % (l, r))

        with open(self.__filename, 'rb') as f:

            #以换行符'\r'拆分所有日志包括首行日志数目
            lines = f.read().split(b'\r')
            i = l

            #读取区间内的日志
            for line in lines[l:r+1]:
                types = unpack('i', line[:4])[0]
                elses = line[4:].decode('gbk')
                print(str(i), types, elses)
                i += 1

    #删除日志
    def delete(self):
        l, r = self.__input_index('输入删除区间, 如:10 20\n')
        confirm = input('是否删除日志%d-%d\n确认(y), 任意键取消.\n' % (l, r))
        if confirm != 'y':
            return
        self.__backup(2, index = (l, r))

    #增加日志
    def add(self):

        #假设操作类型为1,用户为administrator
        types = 1
        user = 'Administrator'.encode('gbk')
        time = datetime.datetime.now().strftime(' %Y-%m-%d, %H:%M ').encode('gbk')
        item = input('输入操作内容:').encode('gbk')

        #转为二进制数据：4个字节int型操作类型，16个字节用户名
        #19个字节日期包括三个空格，任意长度操作内容
        log = pack('i16s19s%ds'%len(item), types, user, time, item) + b'\r'
        self.__backup(1, log = log)

    #修改日志
    def change(self):
        try:
            index = int(input('输入待修改日志序号, 如:10\n'))
            while index < 1 or index > self.__count:
                index = int(input('输入无效, 请重新输入:'))
        except:
            print('输入错误!')
            return

        #假设只修改操作内容
        item = input('修改操作内容为:').encode('gbk')
        log = pack('%ds'%len(item), item) + b'\r'
        self.__backup(3, index = (index,), log = log)

    #移动日志
    def move(self):
        index = self.__input_index(
            '输入待移动日志位置和目标位置, 如:10 20\n',
            mflag = True
        )
        self.__backup(4, index = index)

    #输入区间，移动操作时左右区间为原始位置和目标位置
    def __input_index(self, string, mflag = False):
        index = str(input(string))
        while(not re.match(r'[1-9]+\d* [1-9]+\d*', index)):
            index = input('输入无效, 请重新输入:')
        index = list(map(int, index.split(' ')))

        #移动操作左右区间不排序
        if mflag:
            return index

        #左右区间排序
        index.sort()
        l = index[0] if index[0] <= self.__count else self.__count
        r = index[1] if index[1] <= self.__count else self.__count
        return l, r

    #通过备份操作日志：1-增加，2-删除，3-修改，4-移动
    def __backup(self, flag, index = (), log = ''):

        #源文件f，新文件nf（二进制读写）
        with open(self.__filename, 'rb') as f:
            with open('tempfile', 'wb+') as nf:

                #增加
                if flag == 1:
                    self.__count += 1

                    #修改首行日志数目
                    nf.write(pack('i', self.__count) + b'\r')

                    #拷贝源文件第6个字节至结束(首行4个字节+1个字节换行)
                    nf.write(f.read()[5:])

                    #追加新条目
                    nf.write(log)
                    print(
                        '成功增加日志:%d %s' % (
                            unpack('i', log[:4])[0],
                            log[4:].decode('gbk')
                        )
                    )

                #删除
                elif flag == 2:
                    self.__count -= index[1] - index[0] + 1

                    #首行
                    nf.write(pack('i', self.__count) + b'\r')

                    #读取全文并拆分
                    lines = list(f.read().strip(b'\r').split(b'\r'))
                    i = 0
                    for line in lines[1:]:
                        i += 1

                        #区间内的日志不写入新文件
                        if i >= index[0] and i <= index[1]:
                            print(
                                '成功删除日志:%d %s' % (
                                    unpack('i', line[:4])[0],
                                    line[4:].decode('gbk')
                                )
                            )
                            continue
                        nf.write(line + b'\r')

                #修改
                elif flag == 3:
                    lines = list(f.read().strip(b'\r').split(b'\r'))
                    i = 0
                    for line in lines:
                        i += 1
                        if i == index[0]+1:
                            print(
                                '成功修改\n%d %s\n为\n%d %s%s' % (
                                    unpack('i', line[:4])[0],
                                    line[4:].decode('gbk'),
                                    unpack('i', line[:4])[0],
                                    line[4:39].decode('gbk'),
                                    log.decode('gbk')
                                )
                            )

                            #前39个字节不变，只修改操作记录
                            nf.write(line[:39] + log)
                            continue
                        nf.write(line + b'\r')

                #移动:原位置index[0]，目标位置index[1]
                elif flag == 4:
                    lines = list(f.read().strip(b'\r').split(b'\r'))
                    i = 0
                    for line in lines:
                        i += 1

                        #目标位置写入待移动日志和此位置原有的日志
                        if i == index[1]+1:

                            #日志下移先原有日志再写待移动日志
                            if index[0] < index[1]:
                                nf.write(line + b'\r')
                                nf.write(lines[index[0]] + b'\r')
                                continue
                            nf.write(lines[index[0]] + b'\r')

                        #原位置跳过
                        if i == index[0]+1:
                            continue
                        nf.write(line + b'\r')

                    print(
                        '成功移动第%d条日志\n%d %s\n至%d行' % (
                            index[0],
                            unpack('i', lines[index[0]][:4])[0],
                            lines[index[0]][4:].decode('gbk'),
                            index[1]
                        )
                    )

                else:
                    return

        #备份
        os.rename(self.__filename, self.__filename + '.bak')
        os.rename('tempfile', self.__filename)

def rewrite_log():
    '''
    格式化日志
    '''
    #2进制读取并以换行符'\r'拆分日志为list
    with open('chrom2000.log', 'rb') as f:
        lines = f.read().split(b'\r')
        lineone = unpack('ii', lines[0])
        print(lineone[0], lineone[1])
        for i in range(1, 10):
            print(lines[i].decode('gbk'), unpack('i', lines[i][-4:])[0])

        #读取首行前四个字节转为十进制int型-1为日志数目
        #读取上一行的后4个字节作为本行的操作类型
        #读取每行前16个字节为用户名
        #第20至38字节为日期包括两个空格
        #第42至末尾为操作记录
        #写入新日志文件new.log
        with open('new.log', 'wb+') as newfile:
            line1 = unpack('i', lines[0][:4])[0]
            types = lines[0][4:]
            newfile.write(pack('i', line1-1) + b'\r')
            for line in lines[1:]:
                user = line[:16].strip(b'\x00')
                user = pack('16s', user)
                date = line[20:38]
                item = line[42:-4]
                newfile.write(types+user+date+b' '+item+b'\r')
                types = line[-4:]

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
    #重写日志
    rewrite_log()

    #创建对象
    FILE_NAME = 'new.log'
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
