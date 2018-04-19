# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Jenkins Tool
Jenkins工具
"""

import time
import sys

from jenkinsapi.jenkins import Jenkins
from common import logcm


def get_jenkins_server(host, user, token):
    """
    连接到Jenkins服务器上
    @param host:主机地址
    @param user:用户名
    @param token:用户Token
    """

    logcm.print_info("Connect to jenkins server : %s" % host)
    server = Jenkins('http://' + host + '/jenkins/', username=user, password=token)

    logcm.print_info("server.version : %s" % server.version, show_header=False)
    logcm.print_info("server.baseurl : %s" % server.baseurl, show_header=False)
    return server


def invoke_job(server, job_name, svn_url, task_no):
    """
    启动JOB
    @param job_name:JOB名称ß
    @param svn_url:SVN的URL路径
    @param task_no:任务号
    @return: 无
    """

    # 如果服务器为空
    if server is None:
        logcm.print_info("Jenkins server is none!", fg='red')
        return None

    if job_name is None:
        logcm.print_info("Jenkins job name is none!", fg='red')
        return None

    if job_name not in server:
        logcm.print_info("Jenkins job name not exist : %s" % job_name, fg='red')
        return None

    # search the job for build
    job = server[job_name]

    # start build the job
    job.invoke(build_params={'url': svn_url, 'TASK_NO': task_no})
    logcm.print_info("Jenkins Job %s is invoked." % job_name)

    sec = 0
    while True:
        job = server.get_job(job_name)
        if sec > 7 and not job.is_running():
            print()
            logcm.print_info("Jenkins Job %s is completed!" % job_name, show_header=False)
            break
        else:
            # 显示进度
            logcm.print_style("#", end='', fg='yellow', bg='black')
            # 随时刷新到屏幕上
            sys.stdout.flush()
            sec += 1
            time.sleep(1)
