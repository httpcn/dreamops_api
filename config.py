#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : httpcn

import os.path

__version__ = '0.0.1'


class Config:
    SECRET_KEY = "0123456789abcdefg"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE = 3600  # 秒

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASS = None
    REDIS_MAXCONN = 10

    # zabbix
    ZABBIX_ADDR = 'http://192.168.3.21/'
    ZABBIX_USER = 'Admin'
    ZABBIX_PWD = 'zabbix'

    # log
    LOG_FILE = os.path.join(os.path.dirname(__file__), 'dreamops.log')


class Settings(Config):
    key_prefix = 'dops'  # 全局key前缀
    ver = "::".join([key_prefix, 'version'])  # 版本信息
    auto_user_id = "::".join([key_prefix, 'auto_user_id'])  # user的id列表
    max_id = "::".join([key_prefix, 'max_id'])  # 最大的user id
    users = "::".join([key_prefix, 'users'])  # user信息表


if __name__ == '__main__':
    print(Settings.users)
