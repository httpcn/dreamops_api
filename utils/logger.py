#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : httpcn

import logging

from config import Config
from utils.helper import cur_time


def dops_log(msg, level='info'):
    dops_logger = logging.getLogger('dreamops')
    handler = logging.FileHandler(Config.LOG_FILE)
    dops_logger.addHandler(handler)

    _msg = f"{cur_time()}:{level}:{msg}"
    if level == 'error':
        dops_logger.error(_msg)
    else:
        dops_logger.warning(_msg)


if __name__ == '__main__':
    dops_log('This is a ERROR message')
