#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CNCRS 非居民金融账户涉税信息报送信息生成工具类
"""

import sys
from common import logcm
from common import xmlcm
from common import dictcm
from common import datecm
from common import checkcm

from cncrs.cncrs_tag import *
from cncrs.cncrs_acc import *


class CNCRSReportMaker:
    """
    CNCRS 报告生成器类
    """

    def __init__(self, chk_rule=None, save_path=None, test=False, last_report=None, **kwargs):
        """
        初始化
        :param chk_rule:校验规则
        :param save_path:保存路径
        :param last_report:上次报告记录
        :param test:是否测试模式
        """
        self.test = test
        self.save_path = save_path
        self.chk_rule = chk_rule
        self.last_report = last_report
        self.check_info("Manager", kwargs)
        # 校验通过保存管理信息
        self.ReportingID = kwargs['ReportingID']
        self.FIID = kwargs['FIID']
        self.ReportingPeriod = kwargs['ReportingPeriod']
        # 新数据列表
        self.new_acc_list = []
        # 修改或删除数据列表
        self.update_acc_list = []
        # 账户记录编号
        self.doc_no = 1

    def check_info(self, chk_key, info, line_no=1):
        """
        根据指定规则字典KEY, 对信息进行校验
        :param chk_key: 规则字典KEY
        :param info: 待校验信息
        :param line_no: 行号
        :return: 无
        """
        check_list = dictcm.get(self.chk_rule, chk_key)
        if check_list:
            # 校验信息
            check_result = checkcm.check_obj_by_list(info, check_list)
            if not check_result.ok:
                logcm.print_info("%s Info Check Failed on line %d! \n%s" % (chk_key, line_no, check_list.msg), fg='red')
                sys.exit()

    def set_acc_list(self, acc_list):
        """
        设置并检验账户信息
        :param acc_list:账户列表
        :return:
        """
        # 账户信息校验
        for i in range(len(acc_list)):
            acc_info = acc_list[i]
            line_no = i + 1
            self.check_info("Account", acc_info, line_no)

            holder_type = acc_info["Account"]["AccountHolderType"]
            if holder_type == "01":
                # 非居民个人客户
                self.check_info("Individual", acc_info["Individual"], line_no)
            else:
                # 机构客户
                self.check_info("Organisation", acc_info["Organisation"], line_no)
                # 有非居民控制人的消极非金融机构
                if holder_type == "02":
                    self.check_info("ControllingPerson", acc_info["ControllingPerson"], line_no)

            # 根据新增和变更加入不同列表
            doc_ref_id = self.get_doc_ref_id(acc_info, line_no)
            acc_obj = CNCRSAccount(acc_info, doc_ref_id=doc_ref_id, test=self.test)
            if acc_obj.new_data:
                self.new_acc_list.append(acc_obj)
            else:
                self.update_acc_list.append(acc_obj)

    def get_doc_ref_id(self, acc_info, line_no):
        """
        取得新的账户记录编号
        :return:编号文本
        """
        # 格式: CN + 4位年份 + 14位金融机构注册码 + 9位序列号
        doc_ref_id = "CN%d%s%09d" % (self.ReportingPeriod.year, self.FIID, line_no)
        # 把文档ID和客户编号关联
        if self.last_report:
            key = str(acc_info["Account"]["AccountNumber"])
            self.last_report[key] = doc_ref_id
        return doc_ref_id

    def get_ref_id(self, new_data, sort_no):
        """
        取得报告唯一编码
        :param new_data:是否新数据
        :param sort_no:编号
        :return:编码文本
        """
        prefix = "TR" if self.test else "RE"
        pn = "N" if new_data else "P"
        ref_id = "%s%s%d%s%08d" % (prefix, self.FIID, self.ReportingPeriod.year + 1, pn, sort_no)
        return ref_id

    def get_header_tag(self, new_data, ref_id, no_data=False):
        """
        生成MessageHeader标签
        :param new_data:是否新数据
        :param sort_no:序号
        :param no_data:是否无数据
        :return:
        """
        header = {
            "ReportingID": self.ReportingID,
            "FIID": self.FIID,
            "ReportingType": "CRS",
            "MessageRefId": ref_id,
            "ReportingPeriod": self.ReportingPeriod,
            "MessageTypeIndic": get_message_type_indic(new_data, no_data),
            "Tmstp": datecm.now_time_str("%Y-%m-%dT%H:%M:%S+08:00")
        }
        return MessageHeaderTag(**header)

    def make_report(self, acc_obj, new_data, sort_no):
        """
        生成报送报告
        :param acc_obj:账户信息
        :param new_data:是否新数据
        :param sort_no:序号
        :return:无
        """

        # 根节点标签
        root = CNCRSRootTag()
        # 文件ID
        ref_id = self.get_ref_id(new_data, sort_no)
        # 添加Header标签
        root.add_sub_tag(self.get_header_tag(new_data, ref_id))

        # 报送组
        group = ReportingGroupTag()
        # 取得账户的标签
        acc = acc_obj.get_tag()
        group.add_sub_tag(acc)
        # 添加报送组标签
        root.add_sub_tag(group)

        # 保存报告
        self.save_report(root, ref_id)

    def save_report(self, root, ref_id):
        """
        保存报告文件
        :param root:根节点对象
        :param ref_id:文件ID
        :return:
        """
        # 转成XML
        tree = root.to_dict()
        xml = xmlcm.dict_to_xml(tree)
        logcm.print_obj(xml, "xml")
        # XML文件输出
        sub_path = "test" if self.test else "prod"
        out_file = "%s/%s/%s.xml" % (self.save_path, sub_path, ref_id)
        xmlcm.dict_to_xml(tree, save_path=out_file)

    def make_all_report(self):
        """
        生成所有报送文件
        :return:
        """
        # 生成新数据报告
        if len(self.new_acc_list) > 0:
            sort_no = 1
            for acc_obj in self.new_acc_list:
                self.make_report(acc_obj, True, sort_no)
                sort_no += 1

        # 生成更新数据报告
        if len(self.update_acc_list) > 0:
            sort_no = 1
            for acc_obj in self.update_acc_list:
                self.make_report(acc_obj, False, sort_no)
                sort_no += 1


def get_message_type_indic(new_data=True, no_data=False):
    """
    取得申报数据类型
    :param new_data: 是否新数据
    :param no_data:是否无申报
    :return:
    """
    if new_data:
        # 新数据
        return "CRS701"
    else:
        if not no_data:
            # 修改或删除数据
            return "CRS702"
        else:
            # 零申报
            return "CRS703"
