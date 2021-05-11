#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : httpcn

import jwt
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from utils.myEnum import CodeEnum
from utils.db_redis import RedisDB
from utils.encrypt import encry
from utils.helper import cur_time
from .token import create_token
from config import Settings as S

login_router = APIRouter()


def id_generator():
    with RedisDB() as rdb:
        rdb.setnx(name=S.max_id, value=99)
        max_id = rdb.incr(name=S.max_id)
        return {"max_id": max_id}


class LoginModel(BaseModel):
    username: str
    password: str = Field(min_length=5, max_length=16, description="密码最小5位最大16")


class RegModel(LoginModel):
    pass


class TokenModel(BaseModel):
    token: str
    args: Optional[List] = None
    kwargs: Optional[Dict] = None


def check_password(password, user_info):
    pwd1 = encry(password + S.SECRET_KEY)
    pwd2 = user_info.get('password')

    return pwd1 == pwd2


def token_required(fun):
    def decorator(body: TokenModel):
        try:
            data = jwt.decode("token.......", S.SECRET_KEY, algorithms=S.ALGORITHM)
            username = data.get('username')
            if username:
                kname = "::".join([S.users, username, 'token'])
                with RedisDB() as rdb:
                    ret = rdb.ttl(name=kname)
                    if ret != -2 or ret != -1:
                        return fun()
        except Exception as e:
            print(e)

    return decorator


@login_router.post('/reg')
def user_reg(body: RegModel):
    res = id_generator()
    uid = res['max_id']
    username = body.username
    kname = "::".join([S.users, username])  # dops::users::admin
    password = encry(body.password + S.SECRET_KEY)
    with RedisDB() as rdb:
        ret = rdb.hsetnx(name=kname, key='uid', value=uid)
        if ret == 1:
            token = create_token(data={"username": username})
            rdb.hmset(name=kname, mapping={
                'password': password,
                'reg_time': cur_time()
            })
            # kname -> dops::users::admin::token
            rdb.set(name="::".join([kname, 'token']), value=token, ex=S.ACCESS_TOKEN_EXPIRE)  # 设置过期时间
            return {'code': CodeEnum.SUCCESS, 'data': {'message': '注册成功'}}
        return {'code': CodeEnum.ERROR, 'data': {'message': '用户可能已经存在'}}


@login_router.post('/login')
def user_login(body: LoginModel):
    username = body.username
    password = body.password
    kname = "::".join([S.users, username])
    with RedisDB() as rdb:
        user_info = rdb.hgetall(name=kname)
        if user_info:
            # pwd = user_info.get('password')
            _k = kname + "::token"
            if check_password(password, user_info):
                token = create_token(data={"username": username})
                rdb.set(name=_k, value=token, ex=S.ACCESS_TOKEN_EXPIRE)
                return {'code': CodeEnum.SUCCESS, 'data': {'token': token}}
            else:
                return {'code': CodeEnum.ERROR, 'data': {'message': "密码不正确"}}
        else:
            return {'code': CodeEnum.ERROR, 'data': {'message': '用户不存在'}}


@login_router.post('/reset_passwod')
def reset_pwd(new_pwd: str, body: TokenModel):
    try:
        data = jwt.decode(body.token, S.SECRET_KEY, algorithms=S.ALGORITHM)
        username = data.get('username')
        with RedisDB() as rdb:
            password = encry(new_pwd + S.SECRET_KEY)
            rdb.hset(name=f"{S.users}::{username}", key='password', value=password)
        return {'code': CodeEnum.SUCCESS, 'data': {'message': '密码已修改'}}
    except Exception as e:
        return {'code': CodeEnum.ERROR, 'data': {'message': '密码修改异常'}}


@login_router.get('/info')
def user_info(token: str = Query(...)):
    return {'code': 20000, 'data': {
        'roles': ['admin'],
        'introduction': 'I am a super administrator',
        'avatar': '',
        'name': 'Super Admin'
    }}


@login_router.post('/logout')
def user_logout():
    return {'code': CodeEnum.SUCCESS, 'data': 'success'}


@login_router.post('/check_token')
@token_required
def check_token(n: int):
    return {'data': n}
