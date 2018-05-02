#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jenkins使用示例。
"""

from common import loadcfgcm
from common.jenkinscm import JenkinsClient

# 配置
default_config = """
{
    "host": "locaohost:8080",
    "user": "xxx",
    "token": "xxxxxxx",
    "jobName": "xxxx",
    "svnUrl": "http://10.xx.x.xxx/svn/xxxxxxx",
    "taskNo": "xxxxx",
}
"""

# 加载配置文件
cfg = loadcfgcm.load("net_jenkins_job.json", default_config)

# 链接到服务器
jenkins = JenkinsClient(cfg)

# 启动JOB
jenkins.invoke(cfg['jobName'], cfg['svnUrl'], cfg['taskNo'])
