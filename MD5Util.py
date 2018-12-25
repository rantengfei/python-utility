import hashlib


async def md5(text):
    return hashlib.md5(text.encode()).hexdigest()


async def md5_salt(text):
    p = hashlib.md5(text.encode('utf-8'))
    p.update('huanqiu'.encode('utf-8'))
    return p.hexdigest()



