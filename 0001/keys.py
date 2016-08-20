import random, string

def keys(num, length = 16):
    chars = string.ascii_letters + string.digits
    f = open('KEYS.txt', '+w')
    for i in range(num):
        key = [random.choice(chars) for i in range(length)]
        f.write(''.join(key) + '\n')
    print("done!")
    f.close()

if __name__ == '__main__':
    keys(100)
    
