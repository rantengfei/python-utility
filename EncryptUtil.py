import base64
import json
from Crypto.Cipher import AES
from urllib.parse import quote, unquote

AESKEY = "De8sM4FZvRCRia4V5wJudw=="
key = base64.b64decode(AESKEY)
cipher = AES.new(key)
BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


def encrypt(data):
    payload = pad(quote(data.encode()))
    cipher_text = escape_symbol(base64.b64encode(cipher.encrypt(payload)).decode())
    return cipher_text


def decrypt(data):
    decrypt_text = cipher.decrypt(base64.b64decode(restore_symbol(data)))
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


if __name__ == '__main__':
    # plaintext = "{'cid': 'huanqiujinrong', 'ckey': 'huanqiujinrong', 'phonenum': '18152149829','target':'product_detail', 'product_code':'04757f50d2e54845b02b890392e287b9'}"
    # encrypted = encrypt(plaintext)
    # print('Encrypted: %s' % encrypted)
    # decrypted = decrypt(encrypted)
    # print('Decrypted: %s' % decrypted)
    monile = "13099230230"
    print(encrypt(monile))

