#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : httpcn

from fastapi import APIRouter
from pydantic import BaseModel
from .token import create_token

login_router = APIRouter()


class LoginModel(BaseModel):
    username: str
    password: str


@login_router.post('/user_login')
def user_login(body: LoginModel):
    return {'code': 200, 'message': 'success', 'token': create_token(data=body.dict())}
