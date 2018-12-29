import aiohttp
import datetime
import logging.config
import uuid
import asyncio

"""
使用方法：
1、使用此工具类时，必须先引入logging_setting工具类
2、将该工具类放到项目util里
"""

# 60 seconds default timeout
DEFAULT_TIMEOUT = 60

DEFAULT_REQUEST = "HQ_REQUEST"
DEFAULT_RESPONSE = "HQ_RESPONSE"

async def post(url, data, headers=None, timeout=DEFAULT_TIMEOUT, req=DEFAULT_REQUEST, res=DEFAULT_RESPONSE):
    current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f'{req}, {uuid.uuid1().hex}, {url}, "POST", {data}, {headers}, {None}, {current}')
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            result = await session.post(url, timeout=timeout, data=data)
            result_text = await result.text()
        except asyncio.TimeoutError as e:
            logging.error(
                f'{res}, {uuid.uuid1().hex}, {url}, "POST", {data}, {headers}, Connection timeout(timeout={timeout})')
            raise (e)
        except Exception as e:
            logging.error(
                f'{res}, {uuid.uuid1().hex}, {url}, "POST", {data}, {headers}, {traceback.format_exc()}')
            raise (e)
        current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f'{res}, {uuid.uuid1().hex}, {url}, "POST", {data}, {headers}, {result_text}, {current}')
        return result


async def get(url, headers=None, timeout=DEFAULT_TIMEOUT, req=DEFAULT_REQUEST, res=DEFAULT_RESPONSE, **kwargs):
    current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f'{req}, {uuid.uuid1().hex}, {url}, "GET", {None}, {headers}, {None}, {current}')
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            result = await session.get(url, data=kwargs, timeout=timeout)
            result_text = await result.text()
        except asyncio.TimeoutError as e:
            logging.error(
                f'{res}, {uuid.uuid1().hex}, {url}, "GET", {None}, {headers}, Connection timeout(timeout={timeout})')
            raise (e)
        except Exception as e:
            logging.error(
                f'{res}, {uuid.uuid1().hex}, {url}, "GET", {None}, {headers}, {traceback.format_exc()}')
            raise (e)
        current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f'{res}, {uuid.uuid1().hex}, {url}, "GET", {None}, {headers}, {result_text}, {current}')
        return result


async def put(self, url, data, headers=None, timeout=DEFAULT_TIMEOUT, req=DEFAULT_REQUEST, res=DEFAULT_RESPONSE):
    current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f'{req}, {uuid.uuid1().hex}, {url}, "PUT", {data}, {headers}, {None}, {current}')
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            result = await session.put(url, timeout=timeout, data=data)
            result_text = await result.text()
        except asyncio.TimeoutError as e:
            logging.error(
                f'{res}, {uuid.uuid1().hex}, {url}, "PUT", {data}, {headers}, Connection timeout(timeout={timeout})')
            raise (e)
        except Exception as e:
            logging.error(
                f'{res}, {uuid.uuid1().hex}, {url}, "PUT", {data}, {headers}, {traceback.format_exc()}')
            raise (e)
        current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f'{res}, {uuid.uuid1().hex}, {url}, "PUT", {data}, {headers}, {result_text}, {current}')
        return result


async def fetch_async(url, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session: #协程嵌套，只需要处理最外层协程即可fetch_async
        async with session.get(url, timeout=2) as resp:
            result = await resp.text()
            return result



