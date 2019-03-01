"""
 @Coding: utf-8
 @Product: financial-zbank
 @Author: rtf
 @Time: 2019-03-01 11:50
 @FileName: test_upload.py
 @Software: PyCharm Community Edition
"""

import os
import aiohttp_fetch
from aiohttp import FormData

'''
注意：需要修改aiohttp/formdata.py 文件中以下两行代码
    def __init__(self, fields=(), quote_fields=True, charset=None, boundary=None):
        self._writer = multipart.MultipartWriter('form-data', boundary)
'''

cur_file_path = os.path.dirname(os.path.realpath(__file__))
file1 = os.path.join(cur_file_path, "resource/test1.jpg")
file2 = os.path.join(cur_file_path, "resource/test2.jpg")

async def upload():
    files = [{"field": "fileList", "filename": os.path.basename(file1), "filepath": file1, "content_type": "image/jpeg"},
                {"field": "fileList", "filename": os.path.basename(file2), "filepath": file2, "content_type": "image/jpeg"}]

    boundary = "-------45962402127348"
    headers = {"Content-Type": f"multipart/form-data;boundary={boundary}"}

    data = FormData(boundary=boundary)
    for file in files:
        data.add_field(file.get("field"),
                       open(file.get("filepath"), 'rb'),
                       filename=file.get("filename"),
                       content_type=file.get("content_type"))

    url = 'http://api.fsp.dev.aitaigroup.com:8080/apiCliService/zbb/upload'
    # url = "http://localhost:9999/"
    res = await aiohttp_fetch.post(url, data=data, headers=headers)
    print(await res.text())

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(upload())