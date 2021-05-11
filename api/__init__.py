#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : httpcn

from .v1.zabbix.zabbix_api import zbx_router
from .v1.ansible.ansible_api import ansible_router
from .v1.open_cloud.cloud_api import cloud_router
from .v1.jenkins.jenkins_api import jenkins_router