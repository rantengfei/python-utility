from EncryptUtil import  decrypt


# 将数据解密换行导出到文件
def dump_to_file(data,filepath):
    data_list = []
    f = open(filepath,'w',encoding='utf-8')
    for d in data:
        jiemi_data = decrypt(d)
        data_list.append(jiemi_data)
    f.write('\n'.join(data_list))
    return data_list


if __name__:
    data = []
    dump_to_file(data,"/home/lyk/Desktop/lyk.txt")