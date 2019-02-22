"""
 @Coding: utf-8
 @Product: python-utility
 @Author: rtf
 @Time: 2019-01-16 10:52
 @FileName: params_validate.py
 @Software: PyCharm Community Edition
"""

"""
 接口参数验证配置
 接口名：[参数列表]
 参数列表： [参数名，参数类型，是否必传]
 validate方法参数说明： api: 接口名，params: 参数（json）
 返回说明：lack_params：缺少必传参数列表; empty_params: 值为空的参数列表; error_params：数据类型错误参数列表;
           error_api_lists: 参数验证配置错误
 使用说明：
 1、from utils.params_validate_decorator import validate_params
 2、在函数上@validate_params([["name", str, True], ["gender", str, True], ["age", int, False]])
"""

from inspect import signature
from functools import wraps
from sanic.response import json


# 非必传参数值为（int: 0, float:0, str: "", list: [], dict: {}）处理
def value_is_null_process(params_value, params_type):
    validate_value = False
    if isinstance(params_value, params_type):
        if params_value == 0 or params_value == "" or params_value == [] or params_value == {}:
            validate_value = True
    return validate_value

# 必传参数值为（str: "", list: [], dict: {}）处理
def value_not_null_process(params_value, param_not_null):
    validate_value = True
    if param_not_null:
        if params_value == "" or params_value == [] or params_value == {}:
            validate_value = False
    return validate_value

# 移除多余参数
def remove_redundant_params(req_params, api_params):
    api_keys = [i[0] for i in api_params]
    param_keys = list(req_params)
    new_params_keys = list(set(param_keys).intersection(set(api_keys)))

    new_params = {}
    for k in new_params_keys:
        new_params[k] = req_params.get(k)
    return new_params

def validate(rule, params):
    if not isinstance(params, dict):
        return False, {"return_code": "1003", "return_msg": "参数类型错误!"}
    if rule:
        lack_params = []
        empty_params = []
        error_params = []
        error_api_lists = []
        for i in rule:
            if len(i) == 3:
                param_name = i[0]
                param_type = i[1]
                param_not_null = i[2]
                param_value = params.get(param_name)
                if param_name not in params and param_not_null:
                    lack_params.append(param_name)
                else:
                    if not value_not_null_process(param_value, param_not_null):
                        empty_params.append(param_name)
                    validate_value = value_is_null_process(param_value, param_type)
                    if not validate_value and not isinstance(param_value, param_type):
                        if param_name in params:
                            if param_value or (not param_value and not param_not_null):
                                error_params.append(param_name)
            else:
                error_api_lists.append(i)

        if error_api_lists:
            return False, {"return_code": "1001", "return_msg": f"{error_api_lists}参数验证配置错误!"}
        if lack_params or empty_params or error_params:
            data = {"lack_params": lack_params, "empty_params": empty_params, "error_params": error_params}
            return False, {"return_code": "1111", "return_msg": data}
    new_params = remove_redundant_params(params, rule)
    return True, {"return_code": "0000", "return_msg": "验证通过!", "params": new_params}

def validate_params(rule):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            request = dict(bound_values.arguments).get("request")
            if request:
                if request.method == "GET":
                    params = request.args
                else:
                    params = request.json
                result, msg = validate(rule, params)
                return json(msg)
            else:
                params = dict(bound_values.arguments).get("params")
                return validate(rule, params)
            return func(*args, **kwargs)
        return wrapper
    return decorate


params_rule = [
        ["test_int", int, True], ["test_str", str, True], ["test_list", list, True],
        ["test_dict", dict, True], ["test_float", float, True], ["test_null", str, False]
    ]
@validate_params(params_rule)
def test(params):
    print("xxxxxxx")


if __name__ == "__main__":
    params = {"ssss": "ss", "test_int": 0, "test_str": "xxx", "test_list": [1, 2, 3], "test_float": 0.1,
              "test_dict": {"name": "rtf", "gender": "male"}, "test_null": "", "xxxx": "xx"}
    print(test(params))
