"""
 @Coding: utf-8
 @Product: python-utility-class
 @Author: rtf
 @Time: 2018-12-25 13:51
 @FileName: dict_repeat.py dict去重
 @Software: PyCharm Community Edition
"""


_dict = [{'a': 123, 'b': 12345}, {'a': 123, 'b': 1234}, {'a': 3222, 'b': 1234}, {'a': 123, 'b': 1234}]


# disorderly
def dict_repeat_disorderly(_dict):
    return [dict(t) for t in set([tuple(d.items()) for d in _dict])]


# orderly
def dict_repeat_orderly(_dict):
    _set = set()
    new_dict = []
    for d in _dict:
        t = tuple(d.items())
        if t not in _set:
            _set.add(t)
            new_dict.append(d)
    return new_dict

if __name__ == '__main__':
    print(dict_repeat_disorderly(_dict))
    print(dict_repeat_orderly(_dict))


