#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : httpcn

from fastapi import APIRouter

ansible_router = APIRouter()

@ansible_router.post('/exec_adhoc')
def exec_adhoc():
    pass

@ansible_router.post('/exec_playbook')
def exec_playhook():
    pass

