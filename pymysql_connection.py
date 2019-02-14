"""
 @Coding: utf-8
 @Product: python-utility
 @Author: rtf
 @Time: 2019-01-14 11:40
 @FileName: pymysql_connection.py
 @Software: PyCharm Community Edition
"""

import pymysql
from config import MYSQL_DB_CONFIG


DB_CONFIG = MYSQL_DB_CONFIG[0].get("master")

CONNECTION = pymysql.connect(host=DB_CONFIG.get("host"),
                             user=DB_CONFIG.get("user"),
                             password=DB_CONFIG.get("password"),
                             db=DB_CONFIG.get("db"),
                             port=DB_CONFIG.get("port"),
                             read_timeout=100,
                             write_timeout=100,
                             charset=DB_CONFIG.get("charset"))


def query(sql, fetch_type="fetch"):
    cursor = CONNECTION.cursor()
    cursor.execute(sql)
    if fetch_type == 'fetch':
        result = cursor.fetchall()
    elif fetch_type == 'fetchrow':
        result = cursor.fetchone()
    elif fetch_type == 'fetchval':
        result = cursor.fetchone()
        result = list(result.values())[0]
        CONNECTION.close()
    return result


def execute(sql):
    cursor = CONNECTION.cursor()
    result = cursor.execute(sql)
    CONNECTION.commit()
    CONNECTION.close()
    return result

if __name__ == '__main__':
    s = query('SELECT * FROM users LIMIT 10')
    print(s)

    s1 = execute("INSERT INTO `leader_board_rule`(`ranking`, `min`, `max`, `periods`) VALUES ('排行榜单第999～9999名', 999, 9999, 9999);")
    print(s1)
