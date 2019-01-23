# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
SSH Client class
SSH客户端共通类
"""

import paramiko
import datetime
import os
import sys
import time

from common import logcm
from common import strcm

NGX_KEYS = ["listen", "server_name", "root", "access_log", "error_log"]
TOMCAT_KEYS = ["docBase"]


class SshClient:
    def __init__(self, ssh_config):
        self.cfg = ssh_config
        self.isConnecting = False
        self.count = 1
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
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接到SSH
            logcm.print_info("Connect SSH to %s:%d with %s / %s" % (self.cfg['ip'], self.cfg['port'], self.cfg['username'], self.cfg['password']))
            sys.stdout.flush()

            self.ssh.connect(self.cfg['ip'], self.cfg['port'], self.cfg['username'], self.cfg['password'], timeout=3)
            # 连接到SFTP
            self.sftp = self.ssh.open_sftp()
            # 连接成功
            self.isConnecting = True
        except Exception as e:
            logcm.print_info("connect Exception : %s" % e, fg='red')

    def addCount(self):
        """

        @return: 无
        """
        self.count += 1

    def __del__(self):
        """
        关闭SSH连接
        @return: 无
        """

        if self.isConnecting:
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

    def exe_cmd_list(self, cmd_list, join_exec=False):
        """
        执行SSH命令列表
        @param cmd_list: 要执行的指令列表
        @return: 命令结果行列表
        """

        lines = []
        logcm.print_info('[Execute Commonds]')

        if not join_exec:
            for cmd in cmd_list:
                # skip empty command
                if not cmd or len(cmd) == 0:
                    continue
                linesCmd = self.exe_cmd(cmd)
                lines += linesCmd
        else:
            cmd = ";".join(cmd_list)
            linesCmd = self.exe_cmd(cmd)
            lines += linesCmd

        return lines

    def exe_cmd(self, cmd):
        lines = []
        try:
            logcm.print_info('Commond exec : %s' % cmd, show_header=False)

            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            for line in stdout.readlines():
                lines.append(line)
                print(line)
                # 随时刷新到屏幕上
                sys.stdout.flush()

        except Exception as e:
            logcm.print_info("Execute Commond Exception : %s" % e, fg='red')
        return lines

    def read_config_dict(self, config_file):
        """
        读取config文件
        :param config_file:配置文件路径
        :return: 配置字典
        """

        config_data = {}

        try:
            remote_file = self.sftp.open(config_file, 'r')
            # read any new lines from the file
            line = remote_file.readline()
            while line:
                line = line.strip('\r\n')
                # 排除注释行
                if not line.startswith("#"):
                    # 数据值
                    dataList = line.split("=");
                    if len(dataList) == 2:
                        key = dataList[0].strip()
                        val = dataList[1].strip()
                        config_data[key] = val
                line = remote_file.readline()
            remote_file.close()

        except Exception as e:
            logcm.print_info("read_config_dict Exception : %s" % e, fg='red')

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
                line = strcm.remove_space(line)
                line = line.rstrip(";").rstrip(" main").rstrip(" crit")
                dataList = line.split(" ")
                if len(dataList) >= 2:
                    key = dataList[0]
                    if key in NGX_KEYS and key not in config_data:
                        config_data[key] = " ".join(dataList[1:])
            line = remote_file.readline()
        remote_file.close()

        return config_data

    def find_tomcat_process(self, keyword):
        """
        查询Tomcat进程
        :param keyword: 关键词
        :return:
        """

        cmd = "ps -ef | grep tomcat"
        lines = self.exe_cmd(cmd)
        for line in lines:
            line = line.strip("\r\n")
            pos = line.find(keyword)
            if pos > 0:
                return True

        return False

    def find_used_space(self):
        """
        查询已用磁盘Space
        :return:
        """

        cmd = "df -h"
        lines = self.exe_cmd(cmd)
        for line in lines:
            line = line.strip("\r\n")
            # 去掉冗余空格
            line = strcm.remove_space(line)
            valList = line.split(" ")
            valLen = len(valList)
            # 根目录
            if valList[valLen - 1] == "/":
                usedSpace = valList[valLen - 2].rstrip("%")
                # logcm.print_obj(usedSpace, "usedSpace")
                return float(usedSpace)

        return None

    def find_cpu_idle(self):
        """
        查询空闲CPU
        :return:
        """

        cmd = " top -b -n1 | grep 'Cpu' "
        lines = self.exe_cmd(cmd)
        for line in lines:
            line = line.strip("\r\n")
            if line.startswith("Cpu"):
                valList = line.split(",")
                cpuIdle = valList[3].replace("%id", "")
                # logcm.print_obj(cpuIdle, "cpuIdle")
                return float(cpuIdle)

        return None

    def find_free_mem(self):
        """
        查询空闲内存内存百分比
        :return:
        """

        cmd = " top -b -n1 | head -5 "
        lines = self.exe_cmd(cmd)
        freeMem = None
        totalMem = None
        cachedMem = None
        for line in lines:
            line = line.strip("\r\n")
            if line.startswith("Mem"):
                valList = line.split(",")
                totalMem = strcm.remove_space(valList[0]).split(" ")[1].rstrip("k")
                freeMem = valList[2].strip().split(" ")[0].rstrip("k")

            if line.startswith("Swap"):
                valList = line.split(",")
                cachedMem = strcm.remove_space(valList[3].strip()).split(" ")[0].rstrip("k")

        if freeMem is not None and cachedMem is not None and totalMem is not None:
            freeRate = (float(freeMem) + float(cachedMem)) * 100 / float(totalMem)
            return float("%.1f" % freeRate)

        return None

    def get_server_time(self):
        """
        取得服务器时间
        :return: 服务器时间
        """
        cmd = 'date "+%Y/%m/%d %H:%M:%S" '
        lines = self.exe_cmd(cmd)
        for line in lines:
            line = line.strip("\r\n")
            logcm.print_obj(line, "line")
            server_time = datetime.datetime.strptime(line, '%Y/%m/%d %H:%M:%S')
            logcm.print_obj(server_time, "date_time", show_header=False)
            return server_time

        return None

    def find_up_days(self):
        """
        查询启动天数
        :return:
        """

        cmd = " top -b -n1 | head -1 "
        lines = self.exe_cmd(cmd)
        for line in lines:
            line = line.strip("\r\n")
            if line.startswith("top "):
                if line.find("days") > 0:
                    valList = line.split(",")
                    days = strcm.remove_space(valList[0]).split(" ")[4]
                    # logcm.print_obj(days, "days")
                    return float(days)
                else:
                    return 1.0

        return None

    def get_mount_map(self, keyword):
        """
        取得挂载Map
        :param keyword:关键词
        :return:
        """

        cmd = " mount | grep %s " % keyword
        lines = self.exe_cmd(cmd)
        mountMap = {}
        for line in lines:
            valList = line.split(" ")
            if len(valList) > 3:
                mountMap[valList[2]] = valList[0]

        return mountMap

    def get_file_list(self, remote_path, suffix="*", maxdepth=1):
        """
        读取远程目录下的文件列表
        :param remote_path:远程路径
        :param suffix:文件后缀
        :param maxdepth:文件层次
        :return: 文件列表（不含路径）
        """

        cmd_list = [
            'find %s -maxdepth %d -type f -name "*.%s"' % (remote_path, maxdepth, suffix)
        ]
        lines = self.exe_cmd_list(cmd_list)
        file_list = []
        for line in lines:
            line = line.strip("\r\n")
            pos = line.rfind("/")
            file_list.append(line[pos + 1:])
        # 排序
        file_list.sort()
        return file_list

    def read_all_nginx_upstream(self, vhost_path):
        """
        读取Nginx配置文件中的upstream
        :param vhost_path:配置文件路径
        :return: 配置字典
        """

        # vhost列表
        vhost_list = self.get_file_list(vhost_path, "conf", 1)

        # upstream字典
        upstream_dict_all = {}
        for vhost in vhost_list:
            upstream_dict = self.read_nginx_upstream(vhost_path + "/" + vhost)
            upstream_dict_all.update(upstream_dict)
        return upstream_dict_all

    def read_nginx_upstream(self, config_file):
        """
        读取Nginx配置文件中的upstream
        :param config_file:配置文件路径
        :return: 配置字典
        """

        remote_file = self.sftp.open(config_file, 'r')
        upstream_data = {}
        isStart = False
        upstreamKey = None
        serverList = []

        # read any new lines from the file
        line = remote_file.readline()
        while line:
            line = line.strip('\r\n').strip()
            # 排除注释行
            if not line.startswith("#"):
                # 去掉冗余空格
                line = strcm.remove_space(line)
                if not isStart:
                    # 查找定义开头部分
                    if line.startswith("upstream "):
                        isStart = True
                        dataList = line.split(" ")
                        upstreamKey = dataList[1].rstrip("{")
                        serverList = []
                else:
                    # 查找服务器
                    if line.startswith("server "):
                        dataList = line.split(" ")
                        serverList.append(dataList[1].rstrip(";"))
                    # 查找定义结尾
                    if line.startswith("}"):
                        upstream_data[upstreamKey] = ";".join(serverList)
                        isStart = False

            line = remote_file.readline()
        remote_file.close()

        return upstream_data

    def read_nginx_proxy_pass(self, config_file):
        """
        读取Nginx配置文件中的upstream
        :param config_file:配置文件路径
        :return: 配置字典
        """

        remote_file = self.sftp.open(config_file, 'r')
        proxyPassList = []

        # read any new lines from the file
        line = remote_file.readline()
        while line:
            line = line.strip('\r\n').strip()
            # 排除注释行
            if not line.startswith("#"):
                # 去掉冗余空格
                line = strcm.remove_space(line)
                # 查找定义开头部分
                if line.startswith("proxy_pass "):
                    dataList = line.split(" ")
                    proxyPassStr = dataList[1].rstrip(";")
                    # 去掉http开头
                    proxyPassStr = proxyPassStr.replace("http://", "")
                    # 去掉相对路径部分
                    pos = proxyPassStr.find("/")
                    if pos > 0:
                        proxyPassStr = proxyPassStr[0:pos]
                    # 去掉$部分
                    pos = proxyPassStr.find("$")
                    if pos > 0:
                        proxyPassStr = proxyPassStr[0:pos]
                    # 避免重复数据
                    if proxyPassStr not in proxyPassList:
                        proxyPassList.append(proxyPassStr)

            line = remote_file.readline()
        remote_file.close()

        return proxyPassList

    def read_tomcat_dict(self, config_file):
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
            #
            if line.startswith("<Context "):
                # 去掉冗余空格
                line = strcm.remove_space(line)
                dataList = line.split(" ")
                for dataItem in dataList:
                    if dataItem.find("=") > 0:
                        propList = dataItem.split("=")
                        key = propList[0]
                        if key in TOMCAT_KEYS and key not in config_data:
                            config_data[key] = propList[1].strip("\"'")

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

    def file_print(self, remote_filename):
        """
        通过SSH监控远程文件新增文本行并输出到控制台
        @param remote_filename: 远程文件路径
        @return: 无
        """

        try:
            for line in self.get_new_lines(remote_filename, 0):
                print(line)
                # 随时刷新到屏幕上
                sys.stdout.flush()

        except Exception as e:
            logcm.print_info("File print Etion : %s - %s" % (e, remote_filename), fg='red')

    def tail_print(self, remote_filename, maxRunTime=600):
        """
        通过SSH监控远程文件新增文本行并输出到控制台
        @param remote_filename: 远程文件路径
        @param maxRunTime: 最大运行时间
        @return: 无
        """

        if remote_filename:
            remote_filename = remote_filename.strip()

        try:
            remote_file_size = -1
            runTime = 0
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
                # 运行时间超过最大时间后，自动退出
                runTime += 0.2
                if runTime > maxRunTime:
                    break

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

    def can_telnet(self, ip, port):
        """
        能否Telnel到指定服务器的指定端口
        :param ip: 服务器IP
        :param port: 服务器端口
        :return: 能：True,否：False
        """

        if ip is None or port is None:
            return False

        # sleep 是为了自动退出， head 是为了避免后续乱码无法解析
        cmd = "(sleep 1;) | telnet %s %s | head -2 " % (ip, port)
        lines = self.exe_cmd(cmd)
        for line in lines:
            line = line.strip("\r\n")
            if line.find("Connected to") >= 0:
                return True
            if line.find("Connection refused") >= 0:
                return False

        return False
