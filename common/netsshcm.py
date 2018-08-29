# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
SSH Client class
SSH客户端共通类
"""

import paramiko
import datetime
import os
import re
import sys
import time

from common import logcm

NGX_KEYS = ["listen", "server_name", "access_log", "error_log"]


class SshClient:
    def __init__(self, ssh_config):
        self.cfg = ssh_config
        # config对象
        # {
        # ip: SSH连接的目标IP地址
        # port: SSH连接的目标端口
        # username: 用户名
        # password: 密码
        # }
        self.connect()

    def connect(self):
        """
        通过SSH连接到指定服务器
        @return: ssh, sftp
        """

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接到SSH
        logcm.print_info("Connect SSH to %s:%d" % (self.cfg['ip'], self.cfg['port']))
        sys.stdout.flush()

        self.ssh.connect(self.cfg['ip'], self.cfg['port'], self.cfg['username'], self.cfg['password'], timeout=5)
        # 连接到SFTP
        self.sftp = self.ssh.open_sftp()

    def __del__(self):
        """
        关闭SSH连接
        @return: 无
        """

        # 关闭SFTP连接
        if self.sftp:
            logcm.print_info("Close sftp connection.")
            self.sftp.close()

        # 关闭SSH连接
        if self.ssh:
            logcm.print_info("Close ssh connection.")
            self.ssh.close()

    def get_remote_path(self, local_path, local_dir, remote_dir):
        """
        取得远程路径
        @param local_path: 本地路径
        @param local_dir: 要上传的本地目录
        @param remote_dir: 要上传到的远程目录
        @return: 远程路径
        """

        relative_path = local_path.replace(local_dir, '').replace('\\', '')
        remote_path = os.path.join(remote_dir, relative_path)
        return remote_path

    def listdir(self, remote_dir):
        """
        通过SSH列出远程目录文件一览
        @param remote_dir: 远程目录
        @return: 文件名数组
        """

        try:
            file_list = self.sftp.listdir(remote_dir)
            file_list.sort()
            return file_list
        except Exception as e:
            logcm.print_info("List dir Exception : %s" % e, fg='red')
            return []

    def upload(self, local_dir, remote_dir):
        """
        通过SSH进行文件上传
        @param local_dir: 要上传的本地目录
        @param remote_dir: 要上传到的远程目录
        @return: 无
        """

        try:
            logcm.print_info('upload file start %s ' % datetime.datetime.now())
            for root, dirs, files in os.walk(local_dir):
                # 遍历目录创建
                for name in dirs:
                    local_path = os.path.join(root, name)
                    remote_path = self.get_remote_path(local_path, local_dir, remote_dir)
                    logcm.print_info('Upload path : %s --> %s ' % (local_path, remote_path))
                    try:
                        self.sftp.mkdir(remote_path)
                        logcm.print_info("Mak dir of remote path : %s" % remote_path)
                    except Exception as e:
                        logcm.print_info("Mak dir Exception : %s" % e, fg='red')

                for file_path in files:
                    local_path = os.path.join(root, file_path)
                    remote_path = self.get_remote_path(local_path, local_dir, remote_dir)
                    logcm.print_info('Upload file : %s --> %s ' % (local_path, remote_path))
                    try:
                        self.sftp.put(local_path, remote_path)
                    except Exception as e:
                        logcm.print_info("Upload file Exception : %s" % e, fg='red')

        except Exception as e:
            logcm.print_info("Upload Exception : %s" % e, fg='red')

    def exe_cmd_list(self, cmd_list):
        """
        执行SSH命令列表
        @param cmd_list: 要执行的指令列表
        @return: 命令结果行列表
        """

        lines = []
        try:
            logcm.print_info('[Execute Commonds]')
            for cmd in cmd_list:
                logcm.print_info('Commond exec : %s' % cmd, show_header=False)

                stdin, stdout, stderr = self.ssh.exec_command(cmd)
                time.sleep(0.5)
                for line in stdout.readlines():
                    print(line)
                    lines.append(line)

        except Exception as e:
            logcm.print_info("Execute Commonds Exception : %s" % e, fg='red')
        return lines

    def read_config_dict(self, config_file):
        """
        读取config文件
        :param config_file:配置文件路径
        :return: 配置字典
        """

        remote_file = self.sftp.open(config_file, 'r')
        config_data = {}
        # read any new lines from the file
        line = remote_file.readline()
        while line:
            line = line.strip('\r\n')
            # 排除注释行
            if not line.startswith("#"):
                # 数据值
                dataList = line.split("=");
                if len(dataList) == 2:
                    config_data[dataList[0].strip()] = dataList[1].strip()
            line = remote_file.readline()
        remote_file.close()

        return config_data

    def read_nginx_dict(self, config_file):
        """
        读取Nginx配置文件
        :param config_file:配置文件路径
        :return: 配置字典
        """

        remote_file = self.sftp.open(config_file, 'r')
        config_data = {}
        # read any new lines from the file
        line = remote_file.readline()
        while line:
            line = line.strip('\r\n').strip()
            # 排除注释行
            if not line.startswith("#"):
                # 去掉冗余空格
                line = " ".join(line.split())
                dataList = line.split(" ");
                if len(dataList) >= 2:
                    key = dataList[0]
                    if key in NGX_KEYS:
                        config_data[key] = dataList[1]
            line = remote_file.readline()
        remote_file.close()

        return config_data

    def get_new_lines(self, remote_filename, remote_file_size):
        """
        通过SSH读取远程文件新增文本行
        @param remote_filename: 远程文件路径
        @param remote_file_size: 远程文件曾经大小
        @return: 新增行
        """

        # Opens the file and reads any new data from it.
        remote_file = self.sftp.open(remote_filename, 'r')
        line_terminators_joined = '\r\n'

        # seek to the latest read point in the file
        remote_file.seek(remote_file_size, 0)

        # read any new lines from the file
        line = remote_file.readline()
        while line:
            yield line.strip(line_terminators_joined)
            line = remote_file.readline()

        remote_file.close()

    def tail_print(self, remote_filename):
        """
        通过SSH监控远程文件新增文本行并输出到控制台
        @param remote_filename: 远程文件路径
        @return: 无
        """

        try:
            remote_file_size = -1
            while 1:
                # 文件统计
                stat_info = self.sftp.stat(remote_filename)
                # 上次文件大小非空时，输出新增行
                if remote_file_size >= 0:
                    # if the file's grown
                    if remote_file_size < stat_info.st_size:
                        for line in self.get_new_lines(remote_filename, remote_file_size):
                            print(line)
                            # 随时刷新到屏幕上
                            sys.stdout.flush()
                    remote_file_size = stat_info.st_size
                else:
                    logcm.print_info("Found remote file (%s) size : %d " % (remote_filename, stat_info.st_size))
                    remote_file_size = stat_info.st_size

                # 休息1秒后再试
                time.sleep(0.2)
        except Exception as e:
            logcm.print_info("Tail print Exception : %s - %s" % (e, remote_filename), fg='red')

    def deploy_server(self, server_path, war_name, local_path):
        """
        通过SSH把本地war包发布到远程Tomcat服务器并重启。
        @param server_path: 远程Tomcat服务器目录
        @param war_name: WAR包名（不含后缀）
        @param local_path: 本地WAR包所在目录
        @return: 无
        """

        logcm.print_info("Deploy war start : %s" % war_name)

        # 停止Tomcat，删除已发布War目录及包
        cmd_stop = []
        cmd_stop.append(server_path + '/bin/shutdown.sh')
        cmd_stop.append('rm -rf ' + server_path + '/webapps/' + war_name)
        cmd_stop.append('rm -rf ' + server_path + '/webapps/' + war_name + '.war')
        self.exe_cmd_list(cmd_stop)

        # 上传War包
        self.upload(local_path, server_path + '/webapps/')

        # 启动Tomcat
        cmd_start = []
        cmd_start.append(server_path + '/bin/startup.sh')
        self.exe_cmd_list(cmd_start)

        logcm.print_info("Deploy war end : %s" % war_name)
