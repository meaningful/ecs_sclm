# -*- coding:utf-8 -*-
import logging

# 是否开启log
# log_enable = True
log_enable = False

# log配置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s -- %(name)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    )


class AppLog(object):

    def __init__(self):
        """
        Do nothing, by default."
        """

    @staticmethod
    def debug(tag, msg):
        if log_enable:
            logging.getLogger(tag).debug(msg)
    
    @staticmethod
    def info(tag, msg):
        if log_enable:
            logging.getLogger(tag).info(msg)
           
    @staticmethod
    def warn(tag, msg):
        if log_enable:
            logging.getLogger(tag).warning(msg)

    @staticmethod
    def error(tag, msg):
        if log_enable:
            logging.getLogger(tag).error(msg)


