#coding:utf-8

from string import printable
import pickle
import os
import base64


DATA = {}
CHAR_TABLE = printable
data_name = 'DATA.dat'
skip_null = lambda new, old : new if new else old
bs_encode = lambda string : base64.encodestring(string.encode()).decode()
bs_decode = lambda string : base64.decodestring(string.encode()).decode()
encryption_match = lambda arg, func : [CHAR_TABLE.index(i) for i in func(arg)]
decryption_match = lambda arg, func : func("".join([CHAR_TABLE[i] for i in arg]))

def shuffle():
    global CHAR_TABLE
    try:
        security_code = [CHAR_TABLE.index(i)/100 for i in input("security code:")]
    except:
        return False
    CHAR_TABLE = list(CHAR_TABLE)
    for i in reversed(range(1, len(CHAR_TABLE))):
        for pos in security_code:
            j = int((i+1) * pos)
            CHAR_TABLE[i], CHAR_TABLE[j] = CHAR_TABLE[j], CHAR_TABLE[i]
    CHAR_TABLE = ''.join(CHAR_TABLE)

def load_data():
    global DATA
    if os.path.isfile(data_name):
        with open(data_name, 'rb') as f:
            try:
                DATA = pickle.load(f)
            except EOFError:
                print("file error!")
            except:
                print("load error!")

def save_data():
    if os.path.isfile(data_name):
        os.rename(data_name, data_name+'.bak')
    with open(data_name, 'wb') as f:
        pickle.dump(DATA, f)

def print_data(account, data):
    print("{0}\n{1}:\n\t{2[0]}\n\t{2[1]}\n\t{2[2]}\n{0}".format(
        '*'*60, account, data))

def encryption(*args):
    try:
        return pickle.dumps([encryption_match(i, bs_encode) for i in args])
    except ValueError:
        print("invalid username or password!")
        return False
    except:
        print("faild!")
        return False

def decryption(account):
    try:
        return [decryption_match(i, bs_decode) for i in pickle.loads(account)]
    except ValueError:
        print("invalid username or password!")
        return False
    except:
        print("faild!")
        return False

def add():
    global DATA
    account = input("account:")
    if account in DATA:
        print("account already exists!")
        return False
    user = input("username:")
    pwd = input("password:")
    notes = input("notes:")
    print_data(account, (user, pwd, notes))
    confirm = input("(y) to confirm, else to cancel.")
    if confirm.upper() == 'Y':
        data = encryption(user, pwd, notes)
        if data:
            DATA[account] = data
            print("successfully added!")

def delete():
    global DATA
    account = input("account:")
    if account in DATA:
        data = decryption(DATA[account])
        if not data:
            return False
        print_data(account, data)
        confirm = input("(y) to confirm, else to cancel.")
        if confirm.upper() == 'Y':
            DATA.pop(account)
            print("successfully deleted!")
    else:
        print("account does not exist!")

def change():
    global DATA
    account = input("account:")
    if account in DATA:
        data = decryption(DATA[account])
        if not data:
            return False
        print_data(account, data)
        user = input("new username:")
        pwd = input("new password:")
        notes = input("new notes:")
        new_data = [skip_null(n, o) for n, o in zip((user, pwd, notes), data)]
        print_data(account, new_data)
        confirm = input("(y) to confirm, else to cancel.")
        if confirm.upper() == 'Y':
            new_data = encryption(new_data[0], new_data[1], new_data[2])
            if new_data:
                DATA[account] = new_data
                print("successfully changed!")
    else:
        print("account does not exist!")

def search():
    account = input("account:")
    if account == '*':
        items = [(k, v) for k, v in DATA.items()]
    else:
        items = [(k, v) for k, v in DATA.items() if account in k]
    if items:
        for item in items:
            data = decryption(item[1])
            if data:
                print_data(item[0], data)
    else:
        print("account does not exist!")


if __name__ == '__main__':

    shuffle()
    load_data()

    while True:
        op = input("input your choice:")
        if op == "a":
            add()
            save_data()
        elif op == "c":
            change()
            save_data()
        elif op == "d":
            delete()
            save_data()
        elif op == "s":
            search()
        elif op == "q":
            break
        else:
            continue
