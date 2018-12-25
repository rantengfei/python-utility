import hashlib


"""
 @Coding: utf-8
 @Product: python-utility-class
 @Author: rtf
 @Time: 2018-12-25 13:47
 @FileName: md5.py
 @Software: PyCharm Community Edition
"""


def md5(text):
    return hashlib.md5(text.encode()).hexdigest()


def md5_salt(salt, text):
    p = hashlib.md5(text.encode('utf-8'))
    p.update(salt.encode('utf-8'))
    return p.hexdigest()


if __name__ == '__main__':
    print(md5("hello world"))
    print(md5_salt("aibili", "hello world"))