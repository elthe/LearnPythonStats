# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
SSH common api
SSH相关共通函数
"""

import paramiko
import datetime
import os
import sys
import time

from common import logcm


def get_ssh_conn(ip, port, username, password):
    """
    通过SSH连接到指定服务器
    @param ip: SSH连接的目标IP地址
    @param port: SSH连接的目标端口
    @param username: 用户名
    @param password: 密码
    @return: ssh, sftp
    """

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接到SSH
    logcm.print_info("Connect SSH to %s:%d" % (ip, port))
    ssh.connect(ip, port, username, password, timeout=5)
    # 连接到SFTP
    sftp = ssh.open_sftp()
    return ssh, sftp


def close_ssh_conn(ssh, sftp):
    """
    关闭SSH连接
    @param ssh: SSH连接
    @param sftp: SFTP连接
    @return: 无
    """

    # 关闭SFTP连接
    if sftp is not None:
        logcm.print_info("Close sftp connection.")
        sftp.close()

    # 关闭SSH连接
    if ssh is not None:
        logcm.print_info("Close ssh connection.")
        ssh.close()


def get_remote_path(local_path, local_dir, remote_dir):
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


def upload(sftp, local_dir, remote_dir):
    """
    通过SSH进行文件上传
    @param sftp: SFTP连接
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
                remote_path = get_remote_path(local_path, local_dir, remote_dir)
                logcm.print_info('Upload path : %s --> %s ' % (local_path, remote_path))
                try:
                    sftp.mkdir(remote_path)
                    logcm.print_info("Mak dir of remote path : %s" % remote_path)
                except Exception as e:
                    logcm.print_info("Mak dir Exception : %s" % e, fg='red')

            for file_path in files:
                local_path = os.path.join(root, file_path)
                remote_path = get_remote_path(local_path, local_dir, remote_dir)
                logcm.print_info('Upload file : %s --> %s ' % (local_path, remote_path))
                try:
                    sftp.put(local_path, remote_path)
                except Exception as e:
                    logcm.print_info("Upload file Exception : %s" % e, fg='red')

    except Exception as e:
        logcm.print_info("Upload Exception : %s" % e, fg='red')


def exe_cmd_list(ssh, cmd_list):
    """
    执行SSH命令列表
    @param ssh: SSH服务器连接
    @param cmd_list: 要执行的指令列表
    @return: 无
    """

    try:
        logcm.print_info('[Execute Commonds]')
        for cmd in cmd_list:
            logcm.print_info('Commond exec : %s' % cmd, show_header=False)

            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.readlines()
            logcm.print_obj(out, 'out')

    except Exception as e:
        logcm.print_info("Execute Commonds Exception : %s" % e, fg='red')


def get_new_lines(sftp, remote_filename, remote_file_size):
    """
    通过SSH读取远程文件新增文本行
    @param sftp: SFTP连接
    @param remote_filename: 远程文件路径
    @param remote_file_size: 远程文件曾经大小
    @return: 新增行
    """

    # Opens the file and reads any new data from it.
    remote_file = sftp.open(remote_filename, 'r')
    line_terminators_joined = '\r\n'

    # seek to the latest read point in the file
    remote_file.seek(remote_file_size, 0)

    # read any new lines from the file
    line = remote_file.readline()
    while line:
        yield line.strip(line_terminators_joined)
        line = remote_file.readline()

    remote_file.close()


def tail_print(sftp, remote_filename, history_size=5000):
    """
    通过SSH监控远程文件新增文本行并输出到控制台
    @param sftp: SFTP连接
    @param remote_filename: 远程文件路径
    @param history_size: 显示历史记录大小
    @return: 无
    """

    try:
        remote_file_size = -1
        while 1:
            # 文件统计
            stat_info = sftp.stat(remote_filename)
            # 上次文件大小非空时，输出新增行
            if remote_file_size >= 0:
                # if the file's grown
                if remote_file_size < stat_info.st_size:
                    for line in get_new_lines(sftp, remote_filename, remote_file_size):
                        print(line)
                        # 随时刷新到屏幕上
                        # sys.stdout.flush()
                remote_file_size = stat_info.st_size
            else:
                logcm.print_info("Found remote file (%s) size : %d " % (remote_filename, stat_info.st_size))
                if history_size < stat_info.st_size:
                    remote_file_size = stat_info.st_size - history_size
                else:
                    remote_file_size = 0

            # 休息1秒后再试
            time.sleep(1)
    except Exception as e:
        logcm.print_info("Tail print Exception : %s" % e, fg='red')


def deploy_server(ssh, sftp, server_path, war_name, local_path):
    """
    通过SSH把本地war包发布到远程Tomcat服务器并重启。
    @param ssh: SSH连接
    @param sftp: SFTP连接
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
    exe_cmd_list(ssh, cmd_stop)

    # 上传War包
    upload(sftp, local_path, server_path + '/webapps/')

    # 启动Tomcat
    cmd_start = []
    cmd_start.append(server_path + '/bin/startup.sh')
    exe_cmd_list(ssh, cmd_start)

    logcm.print_info("Deploy war end : %s" % war_name)
