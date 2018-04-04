# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
SSH Tool api
SSH工具类
"""

import paramiko
import threading
import datetime
import os
import time


class SshClient:
    # SSH主机地址
    ip = None
    # SSH主机端口
    port = None
    # 用户名
    username = None
    # 密码
    passwd = None
    # SSH连接对象
    ssh = None
    # SFTP连接对象
    sftp = None

    def __init__(self, _ip, _username='root', _passwd='lead1234#', port=21312):
        """
        构造方法
        @param _ip: SSH连接的目标IP地址
        @param _username: 用户名
        @param _passwd:密码
        @param port:端口
        """
        # 服务器设置
        self.ip = _ip
        self.port = port
        self.username = _username
        self.passwd = _passwd
        self.connect()

    def __del__(self):
        # 关闭SFTP连接
        if self.sftp is not None:
            self.sftp.close()
            print('.....sftp is closed.....' + self.ip)
        # 关闭SSH连接
        if self.ssh is not None:
            self.ssh.close()
            print('.....ssh is closed.....' + self.ip)

    """
    " 连接到SSH服务器
    @return: 无
    """

    def connect(self):
        print()
        print('connect to ip ' + self.ip)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接到SSH
        self.ssh.connect(self.ip, self.port, self.username, self.passwd, timeout=5)
        # 连接到SFTP
        self.sftp = self.ssh.open_sftp()
        print()

    def upload(self, local_dir, remote_dir):
        """
        通过SSH进行文件上传
        @param local_dir: 要上传的本地目录
        @param remote_dir: 要上传到的远程目录
        @return: 无
        """

        try:
            print('upload file start %s ' % datetime.datetime.now())
            for root, dirs, files in os.walk(local_dir):
                print('[%s][%s][%s]' % (root, dirs, files))
                for file_path in files:
                    local_file = os.path.join(root, file_path)
                    print(11, '[%s][%s][%s][%s]' % (root, file_path, local_file, local_dir))
                    a = local_file.replace(local_dir, '').replace('\\', '/').lstrip('/')
                    print('01', a, '[%s]' % remote_dir)
                    remoteFile = os.path.join(remote_dir, a)
                    print(22, remoteFile)
                    try:
                        self.sftp.put(local_file, remoteFile)
                    except Exception as e:
                        self.sftp.mkdir(os.path.split(remoteFile)[0])
                        self.sftp.put(local_file, remoteFile)
                        print("66 upload %s to remote %s" % (local_file, remoteFile))
                for name in dirs:
                    local_path = os.path.join(root, name)
                    print(0, local_path, local_dir)
                    a = local_path.replace(local_dir, '').replace('\\', '')
                    print(1, a)
                    print(1, remote_dir)
                    remote_path = os.path.join(remote_dir, a)
                    print(33, remote_path)
                    try:
                        self.sftp.mkdir(remote_path)
                        print(44, "mkdir path %s" % remote_path)
                    except Exception as e:
                        print(55, e)
            print('77,upload file success %s ' % datetime.datetime.now())
        except Exception as e:
            print(88, e)

    def exe_cmd_list(self, cmd_list):
        """
        执行SSH命令列表
        @param cmd_list: 要执行的指令列表
        @return: 无
        """

        try:
            print('\n[Execute Commonds]\n')
            for cmd in cmd_list:
                print('Commond send >>>>> ' + cmd)
                print()
                stdin, stdout, stderr = self.ssh.exec_command(cmd)
                out = stdout.readlines()
                print('Console output >>>>>>>>>>>>>>>>>>>')
                # 屏幕输出
                for o in out:
                    print(o)
                print('<<<<<<<<<<<<< output End')
                print()
        except Exception as e:
            print(88, e)

    def deploy_server(self, server_path, war_name, local_path):
        """
        通过SSH把本地war包发布到远程Tomcat服务器并重启。
        @param server_path: 远程Tomcat服务器目录
        @param war_name: WAR包名（不含后缀）
        @param local_path: 本地WAR包所在目录
        @return: 无
        """

        print('--------------------------------------')
        print('\nDeploy [' + war_name + '] Start >>>>>>>>>>>>>>>>>>>\n')

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

        print('Deploy [' + war_name + '] End')
        print('--------------------------------------')
        print()

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
                if remote_file_size > 0:
                    # if the file's grown
                    if remote_file_size < stat_info.st_size:
                        for line in self.get_new_lines(remote_filename, remote_file_size):
                            print(line)

                remote_file_size = stat_info.st_size
                # 休息1秒后再试
                time.sleep(1)
        except Exception as e:
            print(88, e)


if __name__ == '__main__':
    # 启动SSH客户端 
    ip = '10.1.xx.xxx'
    sshClient = SshClient(ip)
    # 发包crmcore
    sshClient.deploy_server('/opt/tomcat_XXX', 'xxxx', r'd:\xxxx\output\xxxx')
    # 查看日志
    sshClient.tail_print('/xxxx/logs/xxxxxx/xxxxxxx.log')
