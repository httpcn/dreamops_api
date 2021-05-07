#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : httpcn

from fastapi import APIRouter
from pydantic import BaseModel, Field
from utils.db_redis import RedisDB
from utils.encrypt import encry
from .token import create_token
from config import Settings as S

login_router = APIRouter()


def id_generator():
    with RedisDB() as rdb:
        _k = "::".join([S.key_prefix, 'auto_user_id'])
        _id = "::".join([S.key_prefix, 'max_id'])
        rdb.setnx(name=_id, value=99)
        max_id = rdb.incr(name=_id)
        user_count = rdb.lrange(name=_k, start=0, end=-1)
        if str(max_id) not in user_count:
            rdb.lpush(_k, max_id)
            return {"max_id": max_id}
        else:
            # 错误的结果
            return {"max_id": 0}


class LoginModel(BaseModel):
    username: str
    password: str = Field(min_length=8, max_length=16, description="密码最小8位最大16")


class RegModel(LoginModel):
    pass


@login_router.post('/reg')
def user_reg(body: RegModel):
    res = id_generator()
    data = {
        "username": body.username,
        "password": encry(body.password + S.SECRET_KEY),
        "uid": res['max_id']
    }
    return {'reg_info': data}


@login_router.post('/login')
def user_login(body: LoginModel):
    with RedisDB() as rdb:
        _k = "::".join([S.key_prefix, 'user'])
        user_info = rdb.hgetall(name=_k)
        print(user_info)

    return {'code': 20000, 'data': {'token': create_token(data=body.dict())}}
