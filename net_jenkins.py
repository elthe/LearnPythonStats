#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jenkins使用示例。
"""

from common import logcm
from common import loadcfgcm
from common.jenkinscm import JenkinsClient

# 配置
default_config = """
{
    "host": "locaohost:8080",
    "user": "xxx",
    "token": "xxxxxxx",
    "jobs": {
        "xxx" : [
            {
                "job_name": "xxxxxxx",
                "svn_url": "http://10.xx.x.xxx/svn/xxxxxxx",
                "task_no": "xxxxx"
            }
        ]
    }
}
"""

# 加载配置文件
cfg = loadcfgcm.load("net_jenkins_job.json", default_config)

# 链接到服务器
jenkins = JenkinsClient(cfg)

dev_jobs = jenkins.get_jobs("dev_build")
logcm.print_obj(dev_jobs, "dev_jobs")

test_jobs = jenkins.get_jobs("build", "dev_build")
logcm.print_obj(test_jobs, "test_jobs")


# 启动JOB
# for job in cfg['jobs']["wealthgateway-test"]:
#     jenkins.invoke(**job)


