#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : httpcn

from datetime import datetime


def cur_time(format='%Y-%m-%d %H:%M:%S'):
    dt = datetime.now()
    return datetime.strftime(dt, dt.strftime(format))

if __name__ == '__main__':
    print(cur_time())