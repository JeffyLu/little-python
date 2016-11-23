#coding:utf-8

class Tea:

    def get(self):

        return 'a cup of tea.'

class Coffee:

    def get(self):

        return 'a cup of coffee.'

class Cake:

    def get(self):

        return 'a piece of cake.'


def get_food(food = None):

    menu = dict(
        tea = Tea,
        coffee = Coffee,
        cake = Cake,
    )

    return menu[food]()

if __name__ == '__main__':

    tea = get_food(food = 'tea')
    coffee = get_food(food = 'coffee')
    cake = get_food(food = 'cake')

    print(tea.get())
    print(coffee.get())
    print(cake.get())

