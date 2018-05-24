#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CNCRS 非居民金融账户涉税信息报送账户信息处理类
"""

import sys
from common import logcm
from common import xmlcm
from common import dictcm
from common import datecm
from common.xmlcm import XmlTag
from common.classcm import BaseObject
from common import checkcm
from common.checkcm import CheckRule

from enum import Enum, unique
from cncrs import cncrs_cm
from cncrs.cncrs_tag import *


class CNCRSAccount:
    """
    CNCRS 账户类
    """

    def __init__(self, acc_info, doc_ref_id=None, test=False):
        """
        初始化
        :param acc_info:账户信息
        :param doc_ref_id:账户记录编号
        :param test:是否测试模式
        """
        self.acc_info = acc_info
        self.doc_ref_id = doc_ref_id
        self.test = test

        # 数据记录状态判断
        self.new_data = (acc_info["Account"]['DueDiligenceInd'] == "是")
        self.closed = (acc_info["Account"]['ClosedAccount'] == "是")
        self.self_cert = (acc_info["Account"]['SelfCertification'] == "是")
        self.updated = (not self.new_data) and (not self.closed)

    def get_doc_type_indic(self):
        """
        取得账户报告的类型
        :return:
        """
        prefix = "T" if self.test else "R"
        if self.new_data:
            type_no = 1
        elif self.closed:
            type_no = 3
        else:
            type_no = 2
        type_indic = "%s%d" % (prefix, type_no)
        return type_indic

    def get_tag(self):
        """
        取得账户信息的标签对象
        :return: 标签对象
        """
        # 报送账户标签
        acc = AccountReportTag()
        # 文档说明子标签
        spec_map = {
            "DocRefId": self.doc_ref_id,
            "DocTypeIndic": self.get_doc_type_indic()
        }
        spec = DocSpecTag(**spec_map)
        acc.add_sub_tag(spec)
        # 账号
        acc.add_sub_tag_by_kv("AccountNumber", self.acc_info["Account"]["AccountNumber"])
        # 是否注销
        if self.closed:
            acc.add_sub_tag_by_kv("ClosedAccount", "true")
        else:
            acc.add_sub_tag_by_kv("ClosedAccount", "false")
        # 账户类别
        if self.new_data:
            acc.add_sub_tag_by_kv("DueDiligenceInd", "N")
        else:
            acc.add_sub_tag_by_kv("DueDiligenceInd", "P")
        # 是否取得账户持有人的自证声明
        if self.self_cert:
            acc.add_sub_tag_by_kv("SelfCertification", "true")
        else:
            acc.add_sub_tag_by_kv("SelfCertification", "false")
        # 账户余额
        amount_tag = MoneyAmountTag("AccountBalance", "CNY", self.acc_info["Account"]["AccountBalance"])
        acc.add_sub_tag(amount_tag)
        # 账户持有人类别
        holder_type = cncrs_cm.convert("key-name", self.acc_info["Account"]["AccountHolderType"])
        acc.add_sub_tag_by_kv("AccountHolderType", holder_type)
        # 开户金融机构名称
        acc.add_sub_tag_by_kv("OpeningFIName", self.acc_info["Account"]["OpeningFIName"])
        # 账户收入
        for payment_type in ["CRS501", "CRS502", "CRS503", "CRS504"]:
            # 收入类型
            key = "Payment_" + payment_type
            if key in self.acc_info["Account"]:
                val = self.acc_info["Account"][key]
                if val is not None and val > 0:
                    # 收入标签
                    payment = PaymentTag(payment_type, "CNY", val)
                    acc.add_sub_tag(payment)

        # 账户持有人信息
        acc_holder = AccountHolderTag()
        if holder_type == "CRS100":
            # 非居民个人标签
            acc_holder.add_sub_tag(self.get_individual_tag())
        else:
            # 金融机构
            acc_holder.add_sub_tag(self.get_organisation_tag())

        # 持有人信息
        acc.add_sub_tag(acc_holder)

        # 非居民控制人
        if holder_type == "CRS101":
            acc.add_sub_tag(self.get_controlling_tag())

        return acc

    def get_individual_tag(self):
        """
        个人信息标签
        :return:
        """
        input_data = self.acc_info["Individual"]
        tag = IndividualTag()
        # 姓名标签
        init_param = {
            "nameType": "OECD202",
            "FirstName": input_data["FirstName"],
            "LastName": input_data["LastName"],
            "NameCN": input_data["NameCN"]
        }
        name = NameTag(**init_param)
        tag.add_sub_tag(name)
        # 性别
        tag.add_sub_tag_by_kv("Gender", cncrs_cm.convert("key-name", input_data["Gender"]), prefix="stc")
        # 地址
        country_code = cncrs_cm.convert("country", input_data["AddressCountryCode"])
        city_en = input_data["AddressCityEN"]
        address_free_en = input_data["AddressFreeEN"]
        address_free_cn = input_data["AddressFreeCN"]
        address = AddressTag("OECD301", country_code, city_en, address_free_en, address_free_cn)
        tag.add_sub_tag(address)
        # 证件类型
        tag.add_sub_tag_by_kv("IDType", cncrs_cm.convert("key-name", input_data["IDType"]), prefix="stc")
        # 证件号码
        tag.add_sub_tag_by_kv("IDNumber", input_data["IDNumber"], prefix="stc")
        # 税收居民国代码
        res_country = cncrs_cm.convert("country", input_data["ResCountryCode"])
        tag.add_sub_tag_by_kv("ResCountryCode", res_country, prefix="stc")
        # 税收识别号
        if "TIN" in input_data:
            tin_code = input_data["TIN"]
            tin = TINTag(res_country, tin_code)
            tag.add_sub_tag(tin)
        # 不提供的理由
        if "Explanation" in input_data:
            tag.add_sub_tag_by_kv("Explanation", input_data["Explanation"], prefix="stc")
        # 国籍
        nationality = cncrs_cm.convert("country", input_data["Nationality"])
        tag.add_sub_tag_by_kv("Nationality", nationality, prefix="stc")
        # 出生信息
        birth_date = cncrs_cm.convert("date", input_data["BirthDate"])
        birth_country = cncrs_cm.convert("country", input_data["BirthCountryCode"])
        birth = BirthInfoTag(birth_date, birth_country)
        tag.add_sub_tag(birth)

        return tag

    def get_organisation_tag(self):
        """
        机构信息标签
        :return:
        """

        input_data = self.acc_info["Organisation"]
        tag = OrganisationTag()
        # 姓名标签
        init_param = {
            "nameType": "OECD205",
            "OrganisationNameEN": input_data["OrganisationNameEN"],
            "OrganisationNameCN": input_data["OrganisationNameCN"]
        }
        name = OrganisationNameTag(**init_param)
        tag.add_sub_tag(name)
        # 地址
        country_code = cncrs_cm.convert("country", input_data["AddressCountryCode"])
        city_en = input_data["AddressCityEN"]
        address_free_en = input_data["AddressFreeEN"]
        address_free_cn = input_data["AddressFreeCN"]
        address = AddressTag("OECD303", country_code, city_en, address_free_en, address_free_cn)
        tag.add_sub_tag(address)
        # 税收居民国代码
        res_country = cncrs_cm.convert("country", input_data["ResCountryCode"])
        tag.add_sub_tag_by_kv("ResCountryCode", res_country, prefix="stc")
        # 税收识别号
        if "TIN" in input_data:
            tin_code = input_data["TIN"]
            tin = TINTag(res_country, tin_code)
            tag.add_sub_tag(tin)
        # 不提供的理由
        if "Explanation" in input_data:
            tag.add_sub_tag_by_kv("Explanation", input_data["Explanation"], prefix="stc")

        return tag

    def get_controlling_tag(self):
        """
        控制人信息标签
        :return:
        """

        input_data = self.acc_info["ControllingPerson"]
        tag = ControllingPersonTag()
        # 姓名标签
        init_param = {
            "nameType": "OECD202",
            "FirstName": input_data["FirstName"],
            "LastName": input_data["LastName"],
            "NameCN": input_data["NameCN"]
        }
        name = NameTag(**init_param)
        tag.add_sub_tag(name)
        # 地址
        country_code = cncrs_cm.convert("country", input_data["AddressCountryCode"])
        city_en = input_data["AddressCityEN"]
        address_free_en = input_data["AddressFreeEN"]
        address_free_cn = input_data["AddressFreeCN"]
        address = AddressTag("OECD301", country_code, city_en, address_free_en, address_free_cn)
        tag.add_sub_tag(address)
        # 税收居民国代码
        res_country = cncrs_cm.convert("country", input_data["ResCountryCode"])
        tag.add_sub_tag_by_kv("ResCountryCode", res_country, prefix="stc")
        # 税收识别号
        if "TIN" in input_data:
            tin_code = input_data["TIN"]
            tin = TINTag(res_country, tin_code)
            tag.add_sub_tag(tin)
        # 不提供的理由
        if "Explanation" in input_data:
            tag.add_sub_tag_by_kv("Explanation", input_data["Explanation"], prefix="stc")

        # 出生信息
        birth_date = cncrs_cm.convert("date", input_data["BirthDate"])
        birth_country = cncrs_cm.convert("country", input_data["BirthCountryCode"])
        birth = BirthInfoTag(birth_date, birth_country)
        tag.add_sub_tag(birth)

        return tag
