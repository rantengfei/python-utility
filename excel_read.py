"""
 @Coding: utf-8
 @Product: financial-huanqiu
 @Author: rtf
 @Time: 2019-01-09 15:51
 @FileName: excel_read.py
 @Software: PyCharm Community Edition
"""


import os
import xlrd

CUR_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
TEST_CASE_DIR = os.path.join(os.path.dirname(CUR_FILE_PATH), "test_ddt/test_case")

class ReadExcel(object):
    def __init__(self, excel_path, sheet_name="Sheet1"):
        excel_path = f"{TEST_CASE_DIR}/{excel_path}"
        self.data = xlrd.open_workbook(excel_path)
        self.table = self.data.sheet_by_name(sheet_name)
        # 获取第一行作为key值
        self.keys = self.table.row_values(0)
        self.row_num = self.table.nrows
        self.col_num = self.table.ncols

    def dict_data(self):
        if self.row_num > 1:
            r = []
            j = 1
            for i in list(range(self.row_num - 1)):
                s = {}
                s['row_num'] = i + 2
                values = self.table.row_values(j)
                for x in list(range(self.col_num)):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j += 1
            return r

if __name__ == "__main__":
    file_path = "case_user.xlsx"
    sheet_name = "Sheet1"
    data = ReadExcel(file_path, sheet_name)
    print(data.dict_data())