# ip工具类

async def get_ip(app, request):
    ip = request.headers.get("x-real-ip") or request.headers.get("x-forwarded-for") or request.ip[0]
    return ip