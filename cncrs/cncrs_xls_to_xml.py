#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把EXCEL报送文件转成XML
"""

from common import logcm
from common import xmlcm
from common import filecm
from common import loadcfgcm

# 配置
# Excel文件名，可以对应到多个Sheet，每个Sheet有一个标题行。
default_config = """
{
    "excel_path" : "/path/to/excel",
    "sheet_name" : "申报表",
    "manager" : {
        "title_line" : 3,
        "data_start_line" : 5,
        "title_group" : {
            "manager" : {
                "start_col" : 0,
                "end_col" : 2,
                "title_map" : {
                    "系统用户账号" : "ReportingID",
                    "金融机构注册码" : "FIID", 
                    "报送年度" : "ReportingPeriod"
                }
            }
        }
    },
    "account" : {
        "title_line" : 10,
        "data_start_line" : 12,
        "title_group" : {
            "account" : {
                "start_col" : 0,
                "end_col" : 11,
                "title_map" : {
                    "基金账号" : "AccountNumber",
                    "账户类型" : "ClosedAccount",
                    "账户类别" : "DueDiligenceInd",
                    "自证声明" : "SelfCertification",
                    "账户余额" : "AccountBalance",
                    "账户持有人" : "AccountHolderType",
                    "开户金融机构名称" : "OpeningFIName",
                    "股息收入金额" : "Payment_CRS501",
                    "利息收入金额" : "Payment_CRS502",
                    "销售或者赎回金融资产总收入金额" : "Payment_CRS503",
                    "其他收入" : "Payment_CRS504"
                }
            },
            "Individual" : {
                "start_col" : 12,
                "end_col" : 25,
                "title_map" : {
                    "客户姓名" : "NameCN",
                    "拼音/英文-姓" : "LastName",
                    "拼音/英文-名" : "FirstName",
                    "客户性别" : "Gender",
                    "出生日期" : "BirthDate",
                    "国籍" : "Nationality",
                    "证件类型" : "IDType",
                    "证件号码" : "IDNumber",
                    "现居地址" : "AddressFreeCN",
                    "拼音/英文-现居地址" : "AddressFreeEN",
                    "出生国" : "BirthCountryCode",
                    "税收居民国" : "ResCountryCode",
                    "纳税识别号" : "TIN",
                    "无纳税识别号理由" : "Explanation"
                }
            },
            "Organisation" : {
                "start_col" : 26,
                "end_col" : 32,
                "title_map" : {
                    "机构名称" : "OrganisationNameCN",
                    "拼音/英文-机构名称" : "OrganisationNameEN",
                    "机构地址" : "AddressFreeCN",
                    "拼音/英文-机构地址" : "AddressFreeEN",
                    "税收居民国" : "ResCountryCode",
                    "纳税识别号" : "TIN",
                    "无纳税识别号理由" : "Explanation"
                }
            },
            "ControllingPerson" : {
                "start_col" : 33,
                "end_col" : 45,
                "title_map" : {
                    "控制人姓名" : "NameCN",
                    "拼音/英文-姓" : "LastName",
                    "拼音/英文-名" : "FirstName",
                    "控制人性别" : "Gender",
                    "出生日期" : "BirthDate",
                    "证件类型" : "IDType",
                    "证件号码" : "IDNumber",
                    "现居地址" : "AddressFreeCN",
                    "拼音/英文-现居地址" : "AddressFreeEN",
                    "出生国" : "BirthCountryCode",
                    "税收居民国" : "ResCountryCode",
                    "纳税识别号" : "TIN",
                    "无纳税识别号理由" : "Explanation"
                }
            }
        }
    }
}
"""

# 加载配置文件
cfg = loadcfgcm.load("cncrs_xls_to_xml.json", default_config, config_path='../config')

# 加载Excel信息
cfg_mng = cfg['manager']
manager_list = filecm.load_excel_dict(cfg['excel_path'], cfg['sheet_name'], cfg_mng['title_line'],
                                      cfg_mng['data_start_line'], cfg_mng['title_group'])
logcm.print_obj(manager_list, "manager_list", show_json=True)

cfg_acc = cfg['account']
acc_list = filecm.load_excel_dict(cfg['excel_path'], cfg['sheet_name'], cfg_acc['title_line'],
                                      cfg_acc['data_start_line'], cfg_acc['title_group'])
logcm.print_obj(acc_list, "acc_list", show_json=True)
