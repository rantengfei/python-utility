from collections import OrderedDict

"""
 @Coding: utf-8
 @Product: python-utility-class
 @Author: rtf
 @Time: 2018-12-25 14:53
 @FileName: params_sort.py
 @Software: PyCharm Community Edition
"""


# 按照ASCII码排序并拼接
def sort_ascii(connector, params):
    params = OrderedDict(sorted(params.items()))
    result = ""
    for key, value in params.items():
        result += f'{connector}{key}={value if value else ""}'
    if result.find(connector) == 0:
        result = result[1:]
    return result


if __name__ == "__main__":
    params = {"name": "rtf", "mobile": "18152149829", "gender": "male"}
    print(f"sort_ascii&:{sort_ascii('&', params)}")
    print(f"sort_ascii|:{sort_ascii('|', params)}")

