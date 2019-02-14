"""
 @Coding: utf-8
 @Product: financial-huanqiu
 @Author: rtf
 @Time: 2018-12-11 11:01
 @FileName: mongodb.py
 @Software: PyCharm Community Edition
"""

import pymongo
from bson.objectid import ObjectId
from config import MONGODB

db_client = pymongo.MongoClient(**MONGODB)
db = db_client[MONGODB.get('authSource')]


def insert(collection, data):
    col = db[collection]
    col.insert(data)


def update(collection, data, obj_id):
    col = db[collection]
    result = col.update({"_id": ObjectId(obj_id)}, {"$set": data}, False, True)
    return result

def update_param(collection, data, param):
    col = db[collection]
    result = col.update(param, {"$set": data}, multi=True)
    return result


def remove(collection, obj_id):
    col = db[collection]
    result = col.remove({"_id": ObjectId(obj_id)})
    return result


def find(collection, condition):
    col = db[collection]
    result = col.find(condition)
    data = []
    for i in result:
        data.append(i)
    return data

def find_one(collection, obj_id):
    col = db[collection]
    result = col.find_one({"_id": ObjectId(obj_id)})
    return result


def count(collection, data):
    col = db[collection]
    result = col.count(data)
    return result


if __name__ == '__main__':
    print(find("users", {}))






