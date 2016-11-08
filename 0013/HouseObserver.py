#coding:utf-8


class Subject:
    '''目标'''

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        '''增加观察者'''

        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        '''删除观察者'''

        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        '''通知观察者'''

        for observer in self._observers:
            if modifier != observer:
                observer.update(self)


class Agent(Subject):
    '''代理商'''

    def __init__(self, name=''):
        Subject.__init__(self)
        self.name = name
        self._amounts_of_house = 0

    @property
    def amounts_of_house(self):
        return self._amounts_of_house

    @amounts_of_house.setter
    def amounts_of_house(self, value):
        '''更新房源, 通知客户'''

        self._amounts_of_house = value
        self.notify()


class Customer:
    '''纯客户'''

    def __init__(self, name):
        self.name = name

    def update(self, subject):
        '''自我更新'''

        print('%s: 我是%s的客户, 他有%d套新房子.' %
              (self.name, subject.name, subject.amounts_of_house))


class Customer_and_Agent(Agent):
    '''既是客户也是代理商'''

    def __init__(self, name):
        Agent.__init__(self, name)

    def update(self, subject):
        '''自我更新并通知客户'''

        print('%s: 我是%s的客户, 他有%d套新房子.' %
              (self.name, subject.name, subject.amounts_of_house))

        print('%s: 我自己也是代理商, 我要通知我的客户们有新房子了.' %
              (self.name))
        self.amounts_of_house = subject.amounts_of_house


def main():
    '''具体应用'''

    #创建一个代理商A
    agent_A = Agent('A代理商')

    #代理商A有三个客户
    customer_A1 = Customer('A1')
    customer_A2 = Customer('A2')
    #客户B自己也是代理商
    customer_AB = Customer_and_Agent('AB')

    #注册新客户
    agent_A.attach(customer_A1)
    agent_A.attach(customer_A2)
    agent_A.attach(customer_AB)


    #代理商B有两个客户
    customer_B1 = Customer('B1')
    customer_B2 = Customer('B2')

    #注册新客户
    customer_AB.attach(customer_B1)
    customer_AB.attach(customer_B2)


    #更新房源
    print('----公告: A代理商有5套新房子----')
    agent_A.amounts_of_house = 5


if __name__ == '__main__':

    main()




