# -*- coding: utf-8 -*-
# __author__ : "wyl"
# __time__ : 2018/9/5 11:11
# __file__ : logger.py

import logging
import sys



def getLoger():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(lineno)s - %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger