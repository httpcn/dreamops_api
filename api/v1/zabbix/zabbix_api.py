#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : httpcn

from fastapi import APIRouter
# from typing import Optional, Dict
# from pydantic import BaseModel
from pyzabbix import ZabbixAPI as ZAPI

from config import Config as C
from utils.logger import dops_log
from utils.myEnum import CodeEnum

zbx_router = APIRouter()


class ZabbixAPI:
    def __init__(self, zbx_addr=C.ZABBIX_ADDR):
        self.client = ZAPI(server=zbx_addr)
        self.client.session.verify = False
        self.client.timeout = 3

        dops_log(f"Zabbix Server: {zbx_addr}")

    def login(self, user=C.ZABBIX_USER, password=C.ZABBIX_PWD):
        try:
            self.client.login(user, password)
        except Exception as e:
            dops_log(f"zabbix login error: {e}")
        else:
            dops_log("zabbix login OK")

    def do_request(self, method, params=None):
        dops_log(f"zabbix request: {method}, {str(params)}")
        return self.client.do_request(method, params)


api_summary = {
    'apiinfo.version': {'params': []},
    'user.get': {'params': {"output": "extend"}},
    'host.get': {'params': []},
    'hostgroup.get': {'params': {"output": "extend"}},
}


def api_request(method):
    zbx = ZabbixAPI()
    zbx.login()
    if method in api_summary.keys():
        params = api_summary[method]['params']
        res = zbx.do_request(method, params)
        if res.get('result', None):
            return {'code': CodeEnum.SUCCESS, 'message': '请求成功', 'method': method, 'data': res.get('result')}
        else:
            return {'code': CodeEnum.SUCCESS, 'message': "zabbix返回消息中不包括'result'", 'method': method, 'data': {}}
    else:
        return {'code': CodeEnum.SUCCESS, 'message': f"{method}不被支持"}


@zbx_router.get('/{api_method}')
def zabbix_api(api_method: str):
    return api_request(api_method)


if __name__ == '__main__':
    zbx = ZabbixAPI()
    zbx.login()
