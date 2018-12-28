import pika
import uuid
import traceback
import pymongo
import pymysql
import logging.config
from sanic import Blueprint
from aredis import StrictRedis
from sanic.response import json

monitor = Blueprint('monitor', url_prefix='/api/monitor')
config = None
"""
 @Coding: utf-8
 @Product: financial-message-service
 @Author: rtf
 @Time: 2018-12-28 13:37
 @FileName: monitoring.py
 @Software: PyCharm Community Edition
"""

"""
使用方法：
1、将该工具类放到项目util里
2、在项目run.py
  (1)引入该工具类： 
     from utils import monitor
  (2)将config传入monitor,
     默认key:(redis: REDIS_CONFIG, rabbit_mq: RABBIT_MQ, mysql: MYSQL_DB_CONFIG, mongodb: MONGODB)
     monitor.config = monitor.from_config(config)
     如key不一致，须传入映射
     monitor.config = monitor.from_config(config, REDIS_CONFIG="REDIS_CONFIG1")
  (3)注册工具类的蓝图
     app.blueprint(monitor.monitor)
3、测试
  http://0.0.0.0:9892/api/monitor/mq
"""

def from_config(c, **kargs):
    return { x if x not in kargs else kargs.get(x) : getattr(c, x) for x in dir(c) if not x.startswith("_") }


@monitor.get("/mq")
def mq(request):
    username = config.get("RABBIT_MQ").get('username')
    password = config.get("RABBIT_MQ").get('password')
    host = config.get("RABBIT_MQ").get('host')
    port = config.get("RABBIT_MQ").get('port')
    if username and password:
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    else:
        parameters = pika.ConnectionParameters(host=host, port=port)
    try:
        connection = pika.BlockingConnection(parameters)
        connection = connection.channel()
    except Exception as e:
        logging.error(f'"MSG_EXCEPTION", {uuid.uuid1().hex}, "RabbitMq connection fail", None, None, None, {traceback.format_exc()}')
        return fail(traceback.format_exc())
    return ok(connection)


@monitor.get("/mysql_master")
def mysql_master(request):
    try:
        db_config = config.get("MYSQL_DB_CONFIG")[0].get("master")
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        sql = f"SELECT TABLE_NAME,TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='{db_config.get('db')}';"
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        logging.error(
            f'"MSG_EXCEPTION", {uuid.uuid1().hex}, "mysql_master connection fail", None, None, None, {traceback.format_exc()}')
        return fail(traceback.format_exc())
    return ok(result)


@monitor.get("/mysql_slave")
def mysql_slave(request):
    try:
        db_config = config.get("MYSQL_DB_CONFIG")[0].get("master")
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        sql = f"SELECT TABLE_NAME,TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='{db_config.get('db')}';"
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        logging.error(
            f'"MSG_EXCEPTION", {uuid.uuid1().hex}, "mysql_master connection fail", None, None, None, {traceback.format_exc()}')
        return fail(traceback.format_exc())
    return ok(result)


@monitor.get("/redis")
def redis(request):
    try:
        client = StrictRedis(config.get("REDIS_CONFIG"))
    except Exception as e:
        logging.error(
            f'"MSG_EXCEPTION", {uuid.uuid1().hex}, "Redis connection fail", None, None, None, {traceback.format_exc()}')
        return fail(traceback.format_exc())
    return ok(client)


@monitor.get("/mongodb")
def mongodb(request):
    try:
        db_client = pymongo.MongoClient(**config.get("MONGODB"))
        db = db_client[config.get("MONGODB").get('authSource')]
        db.command("ping")
        cols = db.list_collection_names()
    except Exception as e:
        logging.error(f'"MSG_EXCEPTION", {uuid.uuid1().hex}, "mongodb", None, None, None, {traceback.format_exc()}')
        return fail(traceback.format_exc())
    return ok(cols)


def ok(data):
    if type(data) == list:
        data = {"list": data}
    return json({"data": data, "return_code": "0000", "return_msg": "成功"})


def fail(data=None, return_code="1111", return_msg="失败"):
    return json({"data": data, "return_code": return_code, "return_msg": return_msg})