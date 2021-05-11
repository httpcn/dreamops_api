#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : httpcn

from datetime import datetime, timedelta
import jwt
from typing import Optional

from config import Config


# def create_token(data: dict, expires_delta: Optional[timedelta] = None):
def create_token(data: dict):
    # if expires_delta:
    #     expire = datetime.utcnow() + expires_delta
    # else:
    #     expire = datetime.utcnow() + timedelta(seconds=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    #
    # data.update({"exp": expire})

    return jwt.encode(data, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
