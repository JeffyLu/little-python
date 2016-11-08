#coding:utf-8

class Cake:
    '''普通蛋糕'''

    def __init__(self):
        self._info = '普通蛋糕'

    @property
    def price(self):
        '''价格'''

        print(self._info + '  50元')
        return 50

    def balance(self):
        '''结算'''

        print('共%d元\n' % self.price)


class Wrapper:
    '''装饰模板'''

    def __init__(self, wrapper):
        '''初始化装饰信息'''

        self._info = ''
        self._wrapper = wrapper
        self._extra_price = 10

    @property
    def price(self):
        '''装饰费用'''

        print('%s  %d元' % (self._info, self._extra_price))
        return self._wrapper.price + self._extra_price

    def balance(self):
        '''结算'''

        print('共%d元\n' % self.price)

class CreamWrapper(Wrapper):
    '''奶油装饰'''

    def __init__(self, wrapper):
        self._info = '添加奶油'
        self._wrapper = wrapper
        self._extra_price = 15

class DesignedWrapper(Wrapper):
    '''设计图案装饰'''

    def __init__(self, wrapper):
        self._info = '添加设计图案'
        self._wrapper = wrapper
        self._extra_price = 10

class FruitWrapper(Wrapper):
    '''水果装饰'''

    def __init__(self, wrapper):
        self._info = '添加水果'
        self._wrapper = wrapper
        self._extra_price = 15

class CandleWrapper(Wrapper):
    '''蜡烛装饰'''

    def __init__(self, wrapper):
        self._info = '添加蜡烛'
        self._wrapper = wrapper
        self._extra_price = 10

class CardWrapper(Wrapper):
    '''卡片装饰'''

    def __init__(self, wrapper):
        self._info = '添加卡片'
        self._wrapper = wrapper
        self._extra_price = 5


def main():
    '''应用'''

    print('*普通蛋糕')
    cake = Cake()
    cake.balance()

    print('*水果奶油蛋糕')
    cake1 = FruitWrapper(CreamWrapper(Cake()))
    cake1.balance()

    print('*添加卡片的水果奶油蛋糕')
    cake2 = CardWrapper(FruitWrapper(CreamWrapper(Cake())))
    cake2.balance()

    print('*添加卡片并且带有蜡烛和设计图案的水果奶油蛋糕')
    cake3 = CardWrapper(CandleWrapper(DesignedWrapper(
        FruitWrapper(CreamWrapper(Cake())))))
    cake3.balance()



if __name__ == '__main__':

    main()



#class CreamWrapper:
#
#    def __init__(self, wrapper):
#        self._info = '添加奶油'
#        self._wrapper = wrapper
#
#    @property
#    def price(self):
#        print(self._info + '  10元')
#        return self._wrapper.price + 10
#
#    def balance(self):
#        print('共%d元' % self.price)
#
#class DesignedWrapper:
#
#    def __init__(self, wrapper):
#        self._info = '添加设计图案'
#        self._wrapper = wrapper
#
#    @property
#    def price(self):
#        print(self._info + '  10元')
#        return self._wrapper.price + 10
#
#    def balance(self):
#        print('共%d元' % self.price)
#
#class FruitWrapper(DesignedWrapper):
#
#    def __init__(self, wrapper):
#        self._info = '添加水果'
#        self._wrapper = wrapper




