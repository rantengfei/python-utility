"""
 @Coding: utf-8
 @Product: financial-huanqiu
 @Author: rtf
 @Time: 2019-01-11 09:28
 @FileName: http_requests.py
 @Software: PyCharm Community Edition
"""

"""
封装requests接口请求方法
"""

def requests_api(s, url, method="post", params=None, headers=None, timeout=5):
    verify = False
    res = {}
    try:
        result = s.request(method=method, url=url, params=params, headers=headers,
                           json=params, verify=verify, timeout=timeout)
        print(result)
        if result:
            res = result.json()
        return res
    except Exception as msg:
        res["return_msg"] = str(msg)
        return res