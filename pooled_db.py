"""
 @Coding: utf-8
 @Product: python-utility
 @Author: rtf
 @Time: 2019-02-14 11:40
 @FileName: pooled_db.py
 @Software: PyCharm Community Edition
"""

import pymysql
from DBUtils.PooledDB import PooledDB
from config import DB_CONFIG


DB_CONFIG = DB_CONFIG[0].get("master")

POOL = PooledDB(
    creator=pymysql,    # 使用链接数据库的模块
    maxconnections=10,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,        # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,        # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,      # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,      # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],      # 开始会话前执行的命令列表
    ping=0,             # ping MySQL服务端，检查是否服务可用。
    **DB_CONFIG
)


def query(sql, fetch_type="fetch"):
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    if fetch_type == 'fetch':
        result = cursor.fetchall()
    elif fetch_type == 'fetchrow':
        result = cursor.fetchone()
    elif fetch_type == 'fetchval':
        result = cursor.fetchone()
        result = list(result.values())[0]
    conn.close()
    return result


def execute(sql):
    conn = POOL.connection()
    cursor = conn.cursor()
    result = cursor.execute(sql)
    conn.commit()
    conn.close()
    return result

if __name__ == '__main__':
    s = query('SELECT * FROM users LIMIT 10')
    print(s)

    s1 = execute("INSERT INTO `leader_board_rule`(`ranking`, `min`, `max`, `periods`) VALUES ('排行榜单第999～9999名', 999, 9999, 9999);")
    print(s1)

