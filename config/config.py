DB_CONFIG = [
    {"master":{'host': '192.168.1.11',
               'user': 'financial',
               'password': 'financial',
               'port': 3306,
               'db': 'financial_huanqiu',
               'use_unicode': True,
               'charset': "utf8"},
    "slave":{'host': '192.168.1.11',
               'user': 'financial',
               'password': 'financial',
               'port': 3306,
               'db': 'financial_huanqiu',
               'use_unicode': True,
               'charset': "utf8"}
     }
]

REDIS_BROKER = "redis://redis:6379/0"
REDIS_CONFIG = {'host': 'redis', 'port': 6379}

# mongodb
MONGODB_HOST = "192.168.1.11"
MONGODB_PORT = "27017"
MONGODB_NAME = "financial_huanqiu"
MONGODB_USER = "huanqiu"
MONGODB_PWD = "financial"

MONGODB = {
    "host": "192.168.1.11",
    "port": 27017,
    "authSource": "financial_huanqiu",
    "username": "huanqiu",
    "password": "financial",
    "serverSelectionTimeoutMS": 5
}

ALLOW_MULTI_LOGIN=True
