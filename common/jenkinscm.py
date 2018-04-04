# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Jenkins Tool class
Jenkins工具类
"""

import time
from jenkinsapi.jenkins import Jenkins


class JenkinsClient:
    # Jenkins主机地址
    host = ''
    # 用户名
    user = ''
    # 用户Token
    token = ''
    # Jenkins服务器
    server = None

    def __init__(self, _host, _user, _token):
        """
        构造方法
        @param _host:主机地址
        @param _user:用户名
        @param _token:用户Token
        """

        self.host = _host
        self.user = _user
        self.token = _token

    def connect(self):
        """
        " 连接到Jenkins服务器上
        @return: 无
        """
        print()
        print('connect to host ' + self.host)
        self.server = Jenkins('http://' + self.host + '/jenkins/', username=self.user, password=self.token)
        print("version is : " + self.server.version)
        print("base url is " + self.server.baseurl)
        print()

    def invoke_job(self, job_name, svn_url, task_no):
        """
        启动JOB
        @param job_name:JOB名称ß
        @param svn_url:SVN的URL路径
        @param task_no:任务号
        @return: 无
        """

        # 如果服务器为空，自动连接
        if self.server is None:
            self.connect()
        # search the job for build
        job = self.server[job_name]
        print('job_name is ' + job_name)
        print('build_trigger_url is ' + job.get_build_triggerurl())
        print()
        # start build the job
        job.invoke(build_params={'url': svn_url, 'TASK_NO': task_no})
        print('new building is started background ...')
        self.check_state(job_name)

    def check_state(self, job_name):
        """
        检查Job执行状态
        @param job_name:JOB名称ß
        @return: 无
        """

        sec = 5
        time.sleep(5)
        # print job info
        while True:
            job = self.server.get_job(job_name)
            print('Check Job running : %s' % (job.is_running()))
            if not job.is_running():
                print("building completed!")
                print()
                break
            else:
                print("building... %d seconds" % sec)
            time.sleep(2)
            sec += 2


if __name__ == '__main__':
    host = '10.xx.xx.xxx:8080'
    user = 'xxxx'
    token = 'xxxxxxxxx'
    jenkins = JenkinsClient(host, user, token)

    svnUrl = 'http://10.xx.x.xxx/svn/xxxxxxx'
    taskNo = 'xxxxx'
    jenkins.invoke_job('xxxxxx_dev_build', svnUrl, taskNo)
