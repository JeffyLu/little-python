#coding:utf8

from string import ascii_uppercase, ascii_lowercase, digits
import random

def get_check_code(len_, mode = (True, True, True)):
    '''check code creater.

    len_ : length of check code.
    mode : tuple type, default (upper=True, lower=True, digit=True).
    example:
    >>> get_check_code(6)
        mCX90t
    >>> get_check_code(4, (False, False, True))
        4820
    >>> get_check_code(4, (True, False, False))
        XMDK
    '''

    if not isinstance(len_, int) or len(mode) != 3:
        raise ValueError

    mode = (True, True, True) if set(mode) == {False} else mode
    chars = ''
    for m, c in zip(mode, (ascii_uppercase, ascii_lowercase, digits)):
        if m:
            chars += c
    return ''.join([random.choice(chars) for i in range(len_)])

if __name__ == '__main__':

    print(get_check_code(4, (True, True, False)))
    print(get_check_code(4, (False, False, True)))
    print(get_check_code(6))
