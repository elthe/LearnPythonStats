# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Jenkins Client Class
Jenkins客户端类
"""

import time
import sys

from jenkinsapi.jenkins import Jenkins
from common import logcm


class JenkinsClient:
    def __init__(self, jenkins_config):
        self.cfg = jenkins_config
        # config对象
        # {
        # host: 主机地址
        # user: 用户名
        # token: 用户Token
        # }
        self.connect()

    def connect(self):
        """
        连接到Jenkins服务器上
        """

        logcm.print_info("Connect to jenkins server : %s" % self.cfg['host'])
        self.server = Jenkins('http://' + self.cfg['host'] + '/jenkins/', username=self.cfg['user'],
                              password=self.cfg['token'])

        logcm.print_info("server.version : %s" % self.server.version, show_header=False)
        logcm.print_info("server.baseurl : %s" % self.server.baseurl, show_header=False)

    def __del__(self):
        """
        关闭连接
        @return: 无
        """

        if self.server is not None:
            logcm.print_info("Close jenkins server.")

    def invoke(self, job_name, svn_url, task_no):
        """
        启动JOB
        @param job_name:JOB名称ß
        @param svn_url:SVN的URL路径
        @param task_no:任务号
        @return: 无
        """

        # 如果服务器为空
        if self.server is None:
            logcm.print_info("Jenkins server is none!", fg='red')
            return None

        if job_name is None:
            logcm.print_info("Jenkins job name is none!", fg='red')
            return None

        if job_name not in self.server:
            logcm.print_info("Jenkins job name not exist : %s" % job_name, fg='red')
            return None

        # search the job for build
        job = self.server[job_name]

        # start build the job
        job.invoke(build_params={'SVN_URL': svn_url, 'TASK_NO': task_no})
        logcm.print_info("Jenkins Job %s is invoked." % job_name)

        sec = 0
        while True:
            job = self.server.get_job(job_name)
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
