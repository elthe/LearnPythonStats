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
from common import strcm


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

    def get_jobs(self, searchKey=None, excludeKey=None):
        """
        按照检索关键词，以及排除关键词来取得取得符合条件的JOB名称一览。
        """
        all_job_list = self.server.get_jobs_list()
        if not searchKey and not excludeKey:
            return all_job_list

        rst_job_list = []
        for job_name in all_job_list:
            if searchKey:
                searchList = searchKey.split(";")
                if not strcm.contains_keys(job_name, searchList):
                    continue
            if excludeKey:
                exludeList = excludeKey.split(";")
                if strcm.contains_keys(job_name, exludeList):
                    continue
            rst_job_list.append(job_name)

        return rst_job_list

    def get_job(self, job_name):
        """
        取得JOB
        @param job_name:JOB名称
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
        return job

    def get_latest_buildno(self, job_name):
        """
        取得最近build版本号
        @param job_name:JOB名称
        @return: build版本号
        """

        job = self.get_job(job_name)

        lgb = job.get_last_good_build()
        logcm.print_obj(lgb, "lgb")

        return lgb.buildno

    def empty_build(self, job_name):
        """
        取得最近build版本号
        @param job_name:JOB名称
        @return: build版本号
        """

        job = self.get_job(job_name)

        job.invoke(build_params={})
        logcm.print_info("Jenkins Job %s is invoked." % job_name)

        self.watch_job(job)

    def get_last_build_param(self, job):
        """
        重复最近一次构建参数
        @param job:JOB
        @return: 无
        """

        lgb = job.get_last_good_build()
        actions = lgb.get_actions()
        params = {pair['name']: pair['value'] for pair in actions["parameters"]}
        logcm.print_obj(params, "params", show_header=False)

        return params

    def repeat_build(self, job_name):
        """
        重复最近一次构建
        @param job_name:JOB名称
        @return: 无
        """

        # 取得JOB对象
        job = self.get_job(job_name)
        # 最近build参数
        params = self.get_last_build_param(job)
        # 使用同样参数再次构建
        job.invoke(build_params=params)
        logcm.print_info("Jenkins Job %s is invoked." % job_name)

        self.watch_job(job)

    def invoke(self, job_name, svn_url, task_no, **kwargs):
        """
        启动JOB
        @param job_name:JOB名称ß
        @param svn_url:SVN的URL路径
        @param task_no:任务号
        @return: 无
        """

        job = self.get_job(job_name)

        # start build the job
        params = {'url': svn_url, 'TASK_NO': task_no, 'svnPath': svn_url}
        logcm.print_obj(params, "params", show_header=False)

        job.invoke(build_params=params)
        logcm.print_info("Jenkins Job %s is invoked." % job_name)

        self.watch_job(job)

    def invoke_task(self, job_name, task_no, **kwargs):
        """
        启动JOB
        @param job_name:JOB名称
        @param task_no:任务号
        @return: 无
        """

        # 取得JOB对象
        job = self.get_job(job_name)
        # 最近build参数
        params = self.get_last_build_param(job)

        # 替换任务号参数
        params["TASK_NO"] = task_no
        logcm.print_obj(params, "params", show_header=False)

        job.invoke(build_params=params)
        logcm.print_info("Jenkins Job %s is invoked." % job_name)

        self.watch_job(job)

    def invoke_tag(self, job_name, tag_name, **kwargs):
        """
        启动JOB
        @param job_name:JOB名称ß
        @param tag_name:GitTag名
        @return: 无
        """

        job = self.get_job(job_name)

        # start build the job
        params = {'GitVersion': tag_name}
        logcm.print_obj(params, "params", show_header=False)

        job.invoke(build_params=params)
        logcm.print_info("Jenkins Job %s is invoked." % job_name)

        self.watch_job(job)

    def watch_job(self, job):
        """
        监视JOB
        @param job:JOB名称
        @return: 无
        """

        if job:
            buildNo = job.get_last_buildnumber() + 1
            consoleUrl = 'http://%s/jenkins/job/%s/%d/console' % ( self.cfg['host'], job.name, buildNo)
            logcm.print_obj(consoleUrl, "Console")

            print("<a class='linkBtn' href='%s' target='_blank'>查看控制台输出</a>" % consoleUrl)

