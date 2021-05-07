#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : httpcn

import hashlib

def encry(raw_str):
    return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
