#!/usr/bin/python
# coding=utf-8
# 计算工具类

from decimal import *
import math


# 计算预期收益
def profit(amount, timelong, rate):
    profit = math.floor(Decimal(str(amount)) * Decimal(str(timelong)) * Decimal(str(rate)) * 100 / 36500) / 100
    # profit = (Decimal(str(amount)) * Decimal(str(timelong)) * Decimal(str(rate)) / 36500).quantize(Decimal('0.00'))
    return profit

# 获取双精度的数字
def get_double_amount(amount):
    if amount == None or amount == "":
        return 0
    doubile_amount = math.floor(Decimal(Decimal(str(amount)) * 100)) / 100
    # doubile_amount = (Decimal(Decimal(str(amount)))).quantize(Decimal('0.00'))
    return doubile_amount

# 获取两个金额的和
def get_sum(amount1, amount2):
    sum = Decimal(str(get_double_amount(amount1))) + Decimal(str(get_double_amount(amount2)))
    return sum

# 获取多个金额的和
def get_sums(amounts):
    sum = 0
    for amount in amounts:
        sum += Decimal(str(get_double_amount(amount)))
    return sum

# 获取两个金额差值
def get_reduce(amount1, amount2):
    reduce = Decimal(str(get_double_amount(amount1))) - Decimal(str(get_double_amount(amount2)))
    return reduce


# 转换百分比
def get_percentage(num):
    if num == None or num == "":
        return "0.00%"
    if Decimal(str(num)) == 0:
        return "0.00%"
    doubile_num = math.floor(Decimal(Decimal(str(num)) * 10000)) / 100
    return str('%.2f'%doubile_num) + "%"


def test():
    # test = int(float('100.00') * float(365 * 9.2 / 36500) * 100) / 100,
    # # test = int(float('100.00') * int('365') * float('9.2') * 100) / 36500 /100
    amount1 = profit(100.00,45,6)
    amount2 = profit(100.00,45,7)
    # amount = get_sum(amount1,amount2)
    a = get_double_amount(amount1)
    b = get_double_amount(amount2)
    amount = get_sum(a, b)
    # amount = amount1 + amount2


if __name__ == '__main__':
    test()