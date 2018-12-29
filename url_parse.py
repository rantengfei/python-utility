from urllib.parse import urlparse

#获取域名
def get_domain(url):
    parts = urlparse(url)
    host = parts.netloc.split(":")[0]
    return host

#获取父域名
def get_parent_domain(url):
    parts = urlparse(url)
    host = parts.netloc.split(":")[0]
    point_num = host.split(".")
    if host != '127.0.0.1' and len(point_num) > 2:
        i = host.find('.')
        host = host[i+1:]
    return host
