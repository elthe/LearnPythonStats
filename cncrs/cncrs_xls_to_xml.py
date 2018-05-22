#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把EXCEL报送文件转成XML
"""

import sys

from common import logcm
from common import datecm
from common import xmlcm
from common import filecm
from common import xlscm
from common import loadcfgcm
from common import checkcm
from common.checkcm import CheckRule

from cncrs.cncrs_cm import CNCRSReportMaker
from cncrs.cncrs_tag import *

# 配置
# Excel文件名，可以对应到多个Sheet，每个Sheet有一个标题行。
default_config = """
{
    "excel_path" : "./template/非居民金融账户涉税信息采集表-测试.xlsx",
    "sheet_name" : "申报表",
    "Manager" : {
        "title_line" : 3,
        "data_start_line" : 5,
        "title_group" : {
            "Manager" : {
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
    "Account" : {
        "title_line" : 10,
        "data_start_line" : 12,
        "title_group" : {
            "Account" : {
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

check_config = """
{
    "Manager" : [
        {
            "key" : "ReportingID",
            "title" : "系统用户账号",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 50}
            }            
        },
        {
            "key" : "FIID",
            "title" : "金融机构注册码",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"fix_len" : 14}
            }
        },
        {
            "key" : "ReportingPeriod",
            "title" : "报送年度",
            "rules" : ["not_null", "date"],
            "rule_args" : {
                "length" : {"fix_month" : 12, "fix_day" : 31, "min_year" : 2017}
            }
        }        
    ],
    "Account" : [
        {
            "key" : "AccountNumber",
            "title" : "基金账号",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 100}
            }
        },
        {
            "key" : "ClosedAccount",
            "title" : "客户类别(是否已注销)",
            "rules" : ["not_null", "in_list"],
            "rule_args" : {
                "in_list" : {"range_list" : ["是", "否"]}
            }
        },
        {
            "key" : "DueDiligenceInd",
            "title" : "账号类别(是否新开账户)",
            "rules" : ["not_null", "in_list"],
            "rule_args" : {
                "in_list" : {"range_list" : ["是", "否"]}
            }
        },
        {
            "key" : "SelfCertification",
            "title" : "自证声明",
            "rules" : ["not_null", "in_list"],
            "rule_args" : {
                "in_list" : {"range_list" : ["是", "否"]}
            }
        },
        {
            "key" : "AccountBalance",
            "title" : "自证声明",
            "rules" : ["not_null", "number"],
            "rule_args" : {
                "number" : {"min_val" : 0}
            }
        },
        {
            "key" : "AccountHolderType",
            "title" : "账户持有人类别",
            "rules" : ["not_null", "in_list"],
            "rule_args" : {
                "in_list" : {"range_list" : ["01", "02", "03", "04"]}
            }
        },
        {
            "key" : "OpeningFIName",
            "title" : "开户金融机构名称",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 200}
            }
        }
    ]    
}
"""

# 加载配置文件
cfg = loadcfgcm.load("cncrs_xls_to_xml.json", default_config, config_path='../config')

# 加载规则字典
chk_cfg = loadcfgcm.load("cncrs_xls_to_xml_chk.json", check_config, config_path='../config')
chk_rule_map = checkcm.load_check_map(chk_cfg)

# 加载Excel管理信息
cfg_mng = cfg['Manager']
mng_list = xlscm.load_excel_dict(cfg['excel_path'], cfg['sheet_name'], cfg_mng['title_line'],
                                 cfg_mng['data_start_line'], cfg_mng['title_group'])
# 管理信息为空判断
if mng_list is None or len(mng_list) == 0:
    logcm.print_info("Manager Info is not set!", fg='red')
    sys.exit()
if len(mng_list) != 1:
    logcm.print_info("Manager Info need only one!", fg='red')
    sys.exit()
mng_info = mng_list[0]["Manager"]
logcm.print_obj(mng_info, "mng_info", show_json=True)

# 加载Excel账户信息
cfg_acc = cfg['Account']
acc_list = xlscm.load_excel_dict(cfg['excel_path'], cfg['sheet_name'], cfg_acc['title_line'],
                                 cfg_acc['data_start_line'], cfg_acc['title_group'])
logcm.print_obj(acc_list, "acc_list", show_json=True)
# 账户信息为空判断
if acc_list is None or len(acc_list) == 0:
    logcm.print_info("Account Info is not set!", fg='red')
    sys.exit()

# 报告生成器
maker = CNCRSReportMaker(save_path="../temp/file", chk_rule=chk_rule_map, test=True, **mng_info)
# 设置账户信息
maker.set_acc_list(acc_list)
# 生成XML报告
maker.make_all_report()
