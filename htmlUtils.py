import re
#html过滤

def html_parsing(content):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', content)
    return dd


if __name__:
    with open('/home/hey/Desktop/环球金融用户服务协议.txt') as file_object:
        contents = file_object.read()
        rs = html_parsing(contents)
