import base64


# base64加密
async def base64Query(string):
    base64_string = base64.b64encode(string.encode("utf-8"))
    base64_string = str(base64_string,'utf-8')
    return base64_string