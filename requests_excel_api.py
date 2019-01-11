"""
 @Coding: utf-8
 @Product: financial-huanqiu
 @Author: rtf
 @Time: 2019-01-10 16:12
 @FileName: requests_excel_api.py
 @Software: PyCharm Community Edition
"""


import os
import requests
from excel_read import ReadExcel
from excel_write import WriteExcel, copy_excel

"""
使用方法（test ddt）：
TEST_REPORT_DIR: 测试报告生成目录
wirte_result：将接口响应结果写入Excel
send_requests: 封装接口请求方法
依赖 excel_read, excel_write
"""


CUR_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
TEST_REPORT_DIR = os.path.join(os.path.dirname(CUR_FILE_PATH), "test_ddt/report")


def send_requests(s, req):
    method = req.get("method")
    params = eval(req["params"]) if req.get("params") else None
    headers =  eval(req.get("headers")) if req.get("headers") else None

    verify = False
    res = {}
    try:
        result = s.request(method=method, url=req.get("url"), params=params, headers=headers, json=params, verify=verify )
        result_data = result.json()
        res['id'] = req.get("id")
        res['row_num'] = req.get("row_num")
        res["status_code"] = str(result.status_code)
        res["text"] = result.json()
        res["times"] = str(result.elapsed.total_seconds())
        if res["status_code"] != "200":
            res["error"] = res.get("text")
        else:
            res["error"] = ""
        res["msg"] = ""
        if str(req.get("check_point")) == str(result_data.get("return_code")):
            res["result"] = "pass"
            res["msg"] = str(result_data)
        else:
            res["result"] = "fail"
            res["msg"] = str(result_data)
        return res
    except Exception as msg:
        res["msg"] = str(msg)
        return res

def wirte_result(result, filename="result.xlsx"):
    row_num = result['row_num']

    filename = f"{TEST_REPORT_DIR}/{filename}"
    wt = WriteExcel(filename)
    wt.write(row_num, 7, result['status_code'])      # 写入返回状态码statuscode,第8列
    wt.write(row_num, 8, result['times'])            # 耗时
    wt.write(row_num, 9, result['error'])            # 状态码非200时的返回信息
    wt.write(row_num, 12, result['result'])          # 测试结果 pass 还是fail
    wt.write(row_num, 11, result['msg'])             # 返回信息


if __name__ == "__main__":
    data = ReadExcel("case_user.xlsx").dict_data()
    copy_excel("case_user.xlsx", "case_user_report.xlsx")
    s = requests.session()
    for i in data:
        res = send_requests(s, i)
        wirte_result(res, filename="case_user_report.xlsx")
