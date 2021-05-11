#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : httpcn

from fastapi import APIRouter

jenkins_router = APIRouter()

@jenkins_router.post('/')
def home():
    pass

@jenkins_router.post('/get_jobs')
def get_jobs():
    pass