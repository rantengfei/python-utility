from collections import OrderedDict
from config import MACKEY

# 按照ASCII码排序
async def sortSource(params):
    # salt
    params["mackey"] = MACKEY
    params = OrderedDict(sorted(params.items()))
    result = ""
    for key, value in params.items():
        result += f'&{key}={value if value else ""}'
    if result.find("&") == 0:
        result = result[1:]
    return result


#json排序
async def sortSign(params):
    params = OrderedDict(sorted(params.items()))
    result = ""
    for key, value in params.items():
        if type(value) == dict:
            second_json = ""
            for second_key, second_value in value.items():
                second_json += "{"+f'{second_key}={second_value if second_value else ""}'+"}"
            value = second_json
        result += f'|{key}={value if value else ""}'
    if result.find("|") == 0:
        result = result[1:]
    return result