import base64
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
    key = base64.b64decode(aes_key)
    cipher = AES.new(key)
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    if not isinstance(data, str):
        data = str(data)
    payload = pad(quote(data.encode()))
    cipher_text = escape_symbol(base64.b64encode(cipher.encrypt(payload)).decode())
    return cipher_text


def decrypt(aes_key, data):
    key = base64.b64decode(aes_key)
    cipher = AES.new(key)
    decrypt_text = cipher.decrypt(base64.b64decode(restore_symbol(data)))
    unpad = lambda s: s[0:-ord(s[-1])]
    cipher_text = unquote(unpad(decrypt_text.decode()))

    return cipher_text


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

    cipher = AES.new(data.encode("utf-8"))
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    payload = pad(quote(data.encode()))
    cipher_text = base64.b64encode(cipher.encrypt(payload)).decode()
    return cipher_text


if __name__ == '__main__':
    data = 0
    key = encrypt_key("gsaibili20181231")
    print(f"encrypt_key: {key}")

    encrypt_data = encrypt(key, data)
    print(f"encrypt_result: {encrypt_data}")

    decrypt_data = decrypt("ScWwbaa0PKIBrjj6yBMZvhfu83py9HPzjTMzuRty/Yo=", encrypt_data)
    print(f"decrypt_result: {decrypt_data} {type(decrypt_data)} ")

