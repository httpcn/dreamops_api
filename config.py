#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : httpcn

class Config:
    SECRET_KEY = "0123456789abcdefg"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 3600

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASS = None
    REDIS_MAXCONN = 10

class Settings(Config):
    key_prefix = 'dops'
