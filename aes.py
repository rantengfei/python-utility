import dict_repeat
import json
from Crypto.Cipher import AES
from urllib.parse import quote, unquote


"""
 @Coding: utf-8
 @Product: python-utility-class
 @Author: rtf
 @Time: 2018-12-25 09:40
 @FileName: aes.py AES加解密
 @Software: PyCharm Community Edition
"""


def encrypt(aes_key, data):
    key = dict_repeat.b64decode(aes_key)
    cipher = AES.new(key)
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    payload = pad(quote(data.encode()))
    cipher_text = escape_symbol(dict_repeat.b64encode(cipher.encrypt(payload)).decode())
    return cipher_text


def decrypt(aes_key, data):
    key = dict_repeat.b64decode(aes_key)
    cipher = AES.new(key)
    decrypt_text = cipher.decrypt(dict_repeat.b64decode(restore_symbol(data)))
    unpad = lambda s: s[0:-ord(s[-1])]
    cipher_text = unquote(unpad(decrypt_text.decode()))
    try:
        decrypt_text = json.loads(cipher_text)
    except Exception as e:
        decrypt_text = cipher_text
    return str(decrypt_text) if type(decrypt_text) == int else decrypt_text


def escape_symbol(content):
    if content.find("+") > 0 or content.find("/") > 0:
        content = content.replace("+", ".")
        content = content.replace("/", "_")
    return content


def restore_symbol(content):
    if content.find(".") > 0 or content.find("_") > 0:
        content = content.replace(".", "+")
        content = content.replace("_", "/")
    return content


def encrypt_key(data):
    # 生成加密密钥
    # 密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用

    cipher = AES.new(b"gsaibili20181231")
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    payload = pad(quote(data.encode()))
    cipher_text = dict_repeat.b64encode(cipher.encrypt(payload)).decode()
    return cipher_text


if __name__ == '__main__':
    mobile = "15682786878"
    print(encrypt_key("aibili"))
    print(encrypt("InqMhe/6v0qZp7Mc98rnVA==", mobile))
    print(decrypt("InqMhe/6v0qZp7Mc98rnVA==", "w_T9hHZRYWKaoyB2rkTXBA=="))

