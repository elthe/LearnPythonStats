#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把EXCEL报送文件转成XML转化器类及配置
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

from cncrs.cncrs_mk import CNCRSReportMaker
from cncrs.cncrs_tag import *

# 配置
# Excel文件名，可以对应到多个Sheet，每个Sheet有一个标题行。
default_config = """
{
    "sheet_name" : "申报表",
    "Manager" : {
        "title_line" : 3,
        "data_start_line" : 5,
        "title_group" : {
            "Manager" : {
                "start_col" : "A",
                "end_col" : "C",
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
                "start_col" : "B",
                "end_col" : "L",
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
                "start_col" : "M",
                "end_col" : "AB",
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
                    "拼音/英文-所在城市" : "AddressCityEN",
                    "现居住国" : "AddressCountryCode",                    
                    "出生国" : "BirthCountryCode",
                    "税收居民国" : "ResCountryCode",
                    "纳税识别号" : "TIN",
                    "无纳税识别号理由" : "Explanation"
                }
            },
            "Organisation" : {
                "start_col" : "AC",
                "end_col" : "AK",
                "title_map" : {
                    "机构名称" : "OrganisationNameCN",
                    "拼音/英文-机构名称" : "OrganisationNameEN",
                    "机构地址" : "AddressFreeCN",
                    "拼音/英文-机构地址" : "AddressFreeEN",
                    "拼音/英文-所在城市" : "AddressCityEN",
                    "机构所在国" : "AddressCountryCode",
                    "税收居民国" : "ResCountryCode",
                    "纳税识别号" : "TIN",
                    "无纳税识别号理由" : "Explanation"
                }
            },
            "ControllingPerson" : {
                "start_col" : "AL",
                "end_col" : "AZ",
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
                    "拼音/英文-所在城市" : "AddressCityEN",
                    "现居住国" : "AddressCountryCode",
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
            "title" : "账户余额",
            "rules" : ["not_null", "number"],
            "rule_args" : {
                "number" : {"min_val" : 0}
            }
        },
        {
            "key" : "AccountHolderType",
            "title" : "账户持有人类别",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "key-name"}
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
    ],
    "Individual" : [
        {
            "key" : "FirstName",
            "title" : "拼音/英文-名",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 100}
            }
        },
        {
            "key" : "LastName",
            "title" : "拼音/英文-姓",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 100}
            }
        },
        {
            "key" : "NameCN",
            "title" : "客户姓名",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 100}
            }
        },
        {
            "key" : "Gender",
            "title" : "性别",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "key-name"}
            }
        },
        {
            "key" : "AddressFreeEN",
            "title" : "拼音/英文-现居地址",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 500}
            }
        },
        {
            "key" : "AddressCityEN",
            "title" : "拼音/英文-所在城市",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 200}
            }
        },
        {
            "key" : "AddressCountryCode",
            "title" : "现居住国",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "country"}
            }
        },
        {
            "key" : "AddressFreeCN",
            "title" : "现居地址",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 500}
            }
        },
        {
            "key" : "BirthCountryCode",
            "title" : "出生国",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "country"}
            }
        },
        {
            "key" : "BirthDate",
            "title" : "出生日期",
            "rules" : ["not_null", "date"],
            "rule_args" : {
                "date" : {"max_year" : 2018}
            }
        },
        {
            "key" : "Nationality",
            "title" : "国籍",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "country"}
            }
        },
        {
            "key" : "IDType",
            "title" : "证件类型",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "key-name"}
            }
        },
        {
            "key" : "IDNumber",
            "title" : "证件号码",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 30}
            }
        },
        {
            "key" : "ResCountryCode",
            "title" : "税收居民国",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "country"}
            }
        },
        {
            "key" : "TIN",
            "title" : "纳税识别号",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 200}
            }
        },
        {
            "key" : "Explanation",
            "title" : "无纳税识别号理由",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 1000}
            }
        }
    ],
    "Organisation" : [        
        {
            "key" : "OrganisationNameCN",
            "title" : "机构名称",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 200}
            }
        },
        {
            "key" : "OrganisationNameCN",
            "title" : "拼音/英文-机构名称",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 200}
            }
        },        
        {
            "key" : "AddressFreeEN",
            "title" : "拼音/英文-机构地址",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 500}
            }
        },
        {
            "key" : "AddressCityEN",
            "title" : "拼音/英文-所在城市",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 200}
            }
        },
        {
            "key" : "AddressCountryCode",
            "title" : "机构所在国",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "country"}
            }
        },
        {
            "key" : "AddressFreeCN",
            "title" : "机构地址",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 500}
            }
        },        
        {
            "key" : "ResCountryCode",
            "title" : "税收居民国",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "country"}
            }
        },
        {
            "key" : "TIN",
            "title" : "纳税识别号",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 200}
            }
        },
        {
            "key" : "Explanation",
            "title" : "无纳税识别号理由",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 1000}
            }
        }
    ],
    "ControllingPerson" : [
        {
            "key" : "FirstName",
            "title" : "拼音/英文-名",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 100}
            }
        },
        {
            "key" : "LastName",
            "title" : "拼音/英文-姓",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 100}
            }
        },
        {
            "key" : "NameCN",
            "title" : "客户姓名",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 100}
            }
        },
        {
            "key" : "Gender",
            "title" : "性别",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "key-name"}
            }
        },
        {
            "key" : "AddressFreeEN",
            "title" : "拼音/英文-现居地址",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 500}
            }
        },
        {
            "key" : "AddressCityEN",
            "title" : "拼音/英文-所在城市",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 200}
            }
        },
        {
            "key" : "AddressCountryCode",
            "title" : "现居住国",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "country"}
            }
        },
        {
            "key" : "AddressFreeCN",
            "title" : "现居地址",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 500}
            }
        },
        {
            "key" : "BirthCountryCode",
            "title" : "出生国",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "country"}
            }
        },
        {
            "key" : "BirthDate",
            "title" : "出生日期",
            "rules" : ["not_null", "date"],
            "rule_args" : {
                "date" : {"max_year" : 2018}
            }
        },        
        {
            "key" : "IDType",
            "title" : "证件类型",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "key-name"}
            }
        },
        {
            "key" : "IDNumber",
            "title" : "证件号码",
            "rules" : ["not_null", "length"],
            "rule_args" : {
                "length" : {"max_len" : 30}
            }
        },
        {
            "key" : "ResCountryCode",
            "title" : "税收居民国",
            "rules" : ["not_null", "regex"],
            "rule_args" : {
                "regex" : {"pattern" : "country"}
            }
        },
        {
            "key" : "TIN",
            "title" : "纳税识别号",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 200}
            }
        },
        {
            "key" : "Explanation",
            "title" : "无纳税识别号理由",
            "rules" : ["length"],
            "rule_args" : {
                "length" : {"max_len" : 1000}
            }
        }
    ]
}
"""

last_report = """
{
    "AccountNumber" : "CNXXXXXXX00001"
}
"""


class CNCRSConverter:
    def __init__(self):
        # 加载配置文件
        self.cfg_xls = loadcfgcm.load("cncrs_xls_to_xml.json", default_config)

        # 加载规则字典
        chk_cfg = loadcfgcm.load("cncrs_xls_to_xml_chk.json", check_config)
        self.chk_rule_map = checkcm.load_check_map(chk_cfg)

        # 加载历史报送
        self.last_report = loadcfgcm.load("cncrs_xls_to_xml_last.json", last_report)

    def xls_to_xml(self, xls_path, save_path, test):
        logcm.print_info("Convert %s to xml start!" % xls_path, fg='green')
        # 加载Excel管理信息
        cfg_mng = self.cfg_xls['Manager']
        mng_list = xlscm.load_excel_dict(xls_path, self.cfg_xls['sheet_name'], cfg_mng['title_line'],
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
        cfg_acc = self.cfg_xls['Account']
        acc_list = xlscm.load_excel_dict(xls_path, self.cfg_xls['sheet_name'], cfg_acc['title_line'],
                                         cfg_acc['data_start_line'], cfg_acc['title_group'])
        logcm.print_obj(acc_list, "acc_list", show_json=True)
        # 账户信息为空判断
        if acc_list is None or len(acc_list) == 0:
            logcm.print_info("Account Info is not set!", fg='red')
            sys.exit()

        # 报告生成器
        maker = CNCRSReportMaker(save_path=save_path, chk_rule=self.chk_rule_map, test=test, last_report=self.last_report,
                                 **mng_info)
        # 设置账户信息
        maker.set_acc_list(acc_list)
        # 生成XML报告
        maker.make_all_report()

        # 更新配置信息
        loadcfgcm.save_cfg_file(self.last_report, "cncrs_xls_to_xml_last.json")
