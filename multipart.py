"""
 @Coding: utf-8
 @Product: python-utility
 @Author: rtf
 @Time: 2019-01-14 16:28
 @FileName: multipart.py
 @Software: PyCharm Community Edition
"""

import requests_toolbelt

BOUNDARY = "----WebKitFormBoundary7MA4YWxkTrZu0gW"

def multipart_encoder(data, boundary=BOUNDARY):
    data = dict((k, str(v)) for k, v in data.items())
    data = requests_toolbelt.MultipartEncoder(boundary=boundary, fields=data)

    headers = {"content-type": data.content_type}
    data = data.to_string().decode()
    return headers, data


if __name__ == "__main__":
    headers, data = multipart_encoder({"name": "rtf", "gender": "male"})
    print(f'===============headers================: \n{headers}')
    print(f'===============data==================: \n{data}')