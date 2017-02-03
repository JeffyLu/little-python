#coding:utf-8

import os
import hashlib
import pickle
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


DATA = {}
FILE_NAME= 'DATA.dat'

skip_null = lambda new, old : new if new else old
padding = lambda text : text + ('\0' * (16-(len(text.encode())%16)))
encrypt = None
decrypt = None

def md5(string):
    m = hashlib.md5()
    try:
        m.update(string.encode())
    except TypeError:
        print('type error!')
        return False
    return m.hexdigest()

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
        data = [encrypt(user), encrypt(pwd), encrypt(notes)]
        DATA[account] = data
        print("successfully added!")

def change():
    global DATA
    account = input("account:")
    if account in DATA:
        data = [decrypt(i) for i in DATA[account]]
        print_data(account, data)
        user = input("new username:")
        pwd = input("new password:")
        notes = input("new notes:")
        new_data = [skip_null(n, o) for n, o in zip((user, pwd, notes), data)]
        print_data(account, new_data)
        confirm = input("(y) to confirm, else to cancel.")
        if confirm.upper() == 'Y':
            DATA[account] = [encrypt(i) for i in new_data]
            print("successfully changed!")
    else:
        print("account does not exist!")

def delete():
    global DATA
    account = input("account:")
    if account in DATA:
        data = [decrypt(i) for i in DATA[account]]
        print_data(account, data)
        confirm = input("(y) to confirm, else to cancel.")
        if confirm.upper() == 'Y':
            DATA.pop(account)
            print("successfully deleted!")
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
            data = [decrypt(i) for i in item[1]]
            print_data(item[0], data)
    else:
        print("account does not exist!")

def save_data():
    if os.path.isfile(FILE_NAME):
        os.rename(FILE_NAME, FILE_NAME+'.bak')
    with open(FILE_NAME, 'wb') as f:
        pickle.dump(DATA, f)

def load_data():
    global DATA, encrypt, decrypt
    key = md5(input('security code:'))
    iv = key[8:24]
    encrypt = lambda text : b2a_hex(
        AES.new(key, AES.MODE_CBC, iv).encrypt(padding(text)))
    decrypt = lambda text : AES.new(
        key, AES.MODE_CBC, iv).decrypt(a2b_hex(text)).decode().rstrip('\0')
    if os.path.isfile(FILE_NAME):
        with open(FILE_NAME, 'rb') as f:
            try:
                DATA = pickle.load(f)
            except pickle.UnpicklingError:
                print('file error!')
                return False
            except:
                print('loading error!')
                return False

def print_data(account, data):
    print("{0}\n{1}:\n\t{2[0]}\n\t{2[1]}\n\t{2[2]}\n{0}".format(
        '*'*60, account, data))


if __name__ == '__main__':

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
