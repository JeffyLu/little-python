#coding:utf-8

import types

class Shop:
    '''超市类'''

    def __init__(self, goods=None, vips=None):
        self._goods = goods
        self._vips = vips

    def change_strategy(self, strategy):
        '''修改促销策略'''

        self._strategy = types.MethodType(strategy, self)

    def _strategy(self, goods):
        '''促销策略'''

        #计算消费金额
        amounts = 0
        for g in goods:
            print('%-10s%8.1f元' % (g, self._goods[g]['price']))
            amounts += self._goods[g]['price']

        #会员积分
        points = amounts / 10
        remark = '无'
        return (amounts, points, remark)

    def balance(self, goods, vip=None):
        '''账单结算'''

        print('\n-----------账  单-----------\n')

        #引用促销策略结算账单
        amounts, points, remark = self._strategy(goods)

        #vip用户输出账单
        if vip is not None and vip in self._vips:
            self._vips[vip]['points'] += points
            print('\n尊贵的%s您好!\n\n  累计消费: %.1f元\n  本次积分: %.1f\
                  \n  累计积分: %.1f\n  备注: %s' %
                  (vip, amounts, points, self._vips[vip]['points'], remark))

        #非vip用户输出账单
        else:
            print('\n亲爱的顾客您好!\n\n  累计消费: %.1f元\n  备注: %s' %
                  (amounts, remark))

        print('\n欢迎下次光临!\n')
        print('----------------------------')




def balance_strategy1(self, goods):
    '''妇女节促销策略'''

    #计算消费金额
    amounts = 0
    for g in goods:

        #女性用品打折8折
        if g == '女性用品':
            print('%-10s%8.1f元 折后%.1f元' %
                  (g, self._goods[g]['price'], self._goods[g]['price']*0.8))
            amounts += self._goods[g]['price']*0.8

        #其余商品正常价格
        else:
            print('%-10s%8.1f元' % (g, self._goods[g]['price']))
            amounts += self._goods[g]['price']

    #会员积分
    points = amounts / 10

    #促销信息
    remark = '妇女节期间女性商品8折'

    return (amounts, points, remark)


def balance_strategy2(self, goods):
    '''国庆节促销策略'''

    #计算消费金额
    amounts = 0
    for g in goods:
        print('%-10s%8.1f元' % (g, self._goods[g]['price']))
        amounts += self._goods[g]['price']

    #双倍会员积分
    points = amounts / 10 * 2

    #促销信息
    remark = '国庆期间双倍会员积分'

    return (amounts, points, remark)


def balance_strategy3(self, goods):
    '''店庆日促销策略'''

    #计算消费金额
    amounts = 0
    for g in goods:
        print('%-10s%8.1f元' % (g, self._goods[g]['price']))
        amounts += self._goods[g]['price']

    #会员积分
    points = amounts / 10

    #促销信息
    remark = '店庆日满100送20, 满200送40, 以此类推无上限赠送抵用券'

    #赠送抵用券
    coupon = int(amounts / 100) * 20
    if coupon != 0:
        remark += '\n\t***恭喜您获得%d元抵用券***' % coupon

    return (amounts, points, remark)


def main():
    '''应用'''

    #初始化超市
    goods = {
        '家用电器' : {'price' : 100},
        '休闲食品' : {'price' : 20},
        '女性用品' : {'price' : 30},
        '儿童玩具' : {'price' : 50},
    }
    vips = {
        'vip1' : {'points' : 0},
        'vip2' : {'points' : 0},
        'vip3' : {'points' : 0},
    }
    #购物清单
    shopping = ['家用电器', '休闲食品', '女性用品', '儿童玩具']
    #创建超市
    shop = Shop(goods, vips)

    print('***  vip1在超市购物  ***')
    shop.balance(shopping, 'vip1')

    print('***  vip1在妇女节期间购物  ***')
    #修改促销策略
    shop.change_strategy(balance_strategy1)
    shop.balance(shopping, 'vip1')

    print('***  vip2在国庆节期间购物  ***')
    #修改促销策略
    shop.change_strategy(balance_strategy2)
    shop.balance(shopping, 'vip2')

    print('***  普通顾客在店庆日购物  ***')
    #修改促销策略
    shop.change_strategy(balance_strategy3)
    shop.balance(shopping)


if __name__ == '__main__':

    main()
