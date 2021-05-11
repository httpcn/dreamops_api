#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : httpcn

from fastapi import APIRouter

cloud_router = APIRouter()

@cloud_router.post('/')
def home():
    pass

@cloud_router.post('/get_price')
def get_price():
    pass
