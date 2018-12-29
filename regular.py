#!/usr/bin/python
# coding=utf-8
# 正则验正工具类

import re
import datetime

# 正则匹配电话号码
def check_phone(phone):
    p2 = re.compile('^(13\d|14[5|6|7|8|9]|15\d|166|17\d|18\d|19\d)\d{8}$')
    phonematch = p2.match(phone)
    if phonematch:
        return True
    else:
        return False
# 正则匹配身份证号
# def check_id_card(id_card):
#     p2 = re.compile('^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$')
#     phonematch = p2.match(id_card)
#     if phonematch:
#         return True
#     else:
#         return False

# Errors=['验证通过!','身份证号码位数不对!','身份证号码出生日期超出范围或含有非法字符!','身份证号码校验错误!','身份证地区非法!']
def check_id_card(idcard):
    Errors = ['验证通过!', '身份证号码位数不对!', '身份证号码出生日期超出范围或含有非法字符!', '身份证号码校验错误!', '身份证地区非法!']
    area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
            "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南",
            "42": "湖北", "43": "湖南",
            "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏",
            "61": "陕西",
            "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
    idcard = str(idcard)
    idcard = idcard.strip()
    idcard_list = list(idcard)
    # 地区校验
    key = idcard[0: 2]  # TODO： cc  地区中的键是否存在
    if key in area.keys():
        if (not area[(idcard)[0:2]]):
            return Errors[4]
    else:
        return Errors[4]
    # 15位身份号码检测
    if (len(idcard) == 15):
        # if ((int(idcard[6:8]) + 1900) % 4 == 0 or ((int(idcard[6:8]) + 1900) % 100 == 0 and (int(idcard[6:8]) + 1900) % 4 == 0)):
        #     erg = re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')  # //测试出生日期的合法性
        # else:
        #     ereg = re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')  # //测试出生日期的合法性
        # if (re.match(ereg, idcard)):
        #     return Errors[0]
        # else:
        #     return Errors[2]
        return Errors[1]
    # 18位身份号码检测
    elif (len(idcard) == 18):
        # 出生日期的合法性检查
        # 闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
        # 平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
        if (int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and int(idcard[6:10]) % 4 == 0)):
            ereg = re.compile(
                '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')  # //闰年出生日期的合法性正则表达式
        else:
            ereg = re.compile(
                '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')  # //平年出生日期的合法性正则表达式
        # //测试出生日期的合法性
        if (re.match(ereg, idcard)):
            # //计算校验位
            S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + (int(idcard_list[1]) + int(
                idcard_list[11])) * 9 + (int(idcard_list[2]) + int(idcard_list[12])) * 10 + (int(
                idcard_list[3]) + int(idcard_list[13])) * 5 + (int(idcard_list[4]) + int(idcard_list[14])) * 8 + (int(idcard_list[5]) + int(idcard_list[15])) * 4 + (int(idcard_list[6]) + int(idcard_list[16])) * 2 + int(
                idcard_list[7]) * 1 + int(idcard_list[8]) * 6 + int(idcard_list[9]) * 3
            Y = S % 11
            M = "F"
            JYM = "10X98765432"
            M = JYM[Y]  # 判断校验位
            if (M == idcard_list[17]):  # 检测ID的校验位
                return Errors[0]
            else:
                return Errors[3]
        else:
            return Errors[2]
    else:
        return Errors[1]


#判断是否成年
def is_adult(birthday):
    current = datetime.datetime.now()
    if current.year - birthday.year < 18:  # 如果年份小于18，直接返回false，未成年
        return False
    elif current.year - birthday.year == 18:  # 如果年份差等于18，则比较月份
        if current.month > birthday.month:   #年份等于18时，当前月份小于出生月份，则返回false，未成年
            return False
        elif current.month == birthday.month:  # 如果月份也相等，则比较日期
            if current.day > birthday.day: #年份等于18，月份相等时，如果当前日期小于出生日期，则返回false，未成年
                return False;
    return True;

#获取地区
def get_area(id_card):
    areas = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
            "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南",
            "42": "湖北", "43": "湖南",
            "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏",
            "61": "陕西",
            "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
    idcard = str(id_card).replace(' ','')
    # 地区校验
    key = idcard[0: 2]  # TODO： cc  地区中的键是否存在
    # area = areas.get(key)
    return key

#获取年龄
def get_age(id_card,birthday=None):
    idcard = str(id_card).replace(' ', '')
    if not birthday:
        birthday = datetime.datetime.strptime(str(idcard[6:10]) + '-' + str(idcard[10:12]) + '-' + str(idcard[12:14]),'%Y-%m-%d')
    else:
        birthday = datetime.datetime.strptime(str(birthday),'%Y-%m-%d')
    current = datetime.datetime.now()
    age = current.year - birthday.year
    if current.month < birthday.month:
        age = age - 1
    else:
        if current.month == birthday.month:
            if current.day < birthday.day:
                age = age - 1
    return age

#获取出生日期
def get_birthday(id_card):
    idcard = str(id_card).replace(' ', '')
    birthday = datetime.datetime.strptime(str(idcard[6:10]) + '-' + str(idcard[10:12]) + '-' + str(idcard[12:14]),'%Y-%m-%d')
    return birthday

if __name__ == '__main__':
    # phone = "18401539507"
    # OK = check_phone(phone)
    # print(str(OK))
    id_card = "620423201711305413"
    print(get_age(id_card,"2017-12-11"))

