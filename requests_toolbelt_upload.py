"""
 @Coding: utf-8
 @Product: python-utility
 @Author: rtf
 @Time: 2019-03-01 15:09
 @FileName: request_upload.py
 @Software: PyCharm Community Edition
"""


import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

cur_file_path = os.path.dirname(os.path.realpath(__file__))
file1 = os.path.join(cur_file_path, "resource/test1.jpg")
file2 = os.path.join(cur_file_path, "resource/test2.jpg")

def upload():
    fileList = [('fileList', ('test1.jpg', open(file1, 'rb'), "image/jpeg")),
                ('fileList', ('test2.jpg', open(file2, 'rb'), "image/jpeg"))]
    m = MultipartEncoder(fields=fileList, boundary="-------45962402127348")
    headers = {"content-type": m.content_type}
    url = 'http://api.fsp.dev.aitaigroup.com:8080/apiCliService/zbb/upload'
    res = requests.post(url, data=m,
                      headers=headers)
    print(res.text)

if __name__ == "__main__":
    upload()