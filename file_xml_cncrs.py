#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CNCRS 非居民金融账户涉税信息报送XML 做成示例
"""

from common import logcm
from common import xmlcm
from common.classcm import BaseObject

from enum import Enum, unique

# 金融机构注册码 14位
FIID = "XXXXXXXXXXXXXX"


@unique
class MessageType(Enum):
    """
    报告类型
    注意：每个报告的账户记录要么全是新数据，要么全部是修改和删除数据，
    不能在同一个报告中混合报送。
    """
    # 新数据，对应的DocType可以为R1或T1
    CRS701 = 'CRS701'
    # 修改或删除数据，对应的DocTypeIndic可以为R2、R3、T2或T3
    CRS702 = 'CRS702'
    # 零申报，金融机构当年无应申报数据时，应作零申报。
    CRS703 = 'CRS703'


@unique
class AccountHolderType(Enum):
    """
    账户持有人类别
    """
    # 非居民个人
    CRS100 = 'CRS100'
    # 有非居民控制人的消极非金融机构
    CRS101 = 'CRS101'
    # 非居民机构，不包括消极非金融机构
    CRS102 = 'CRS102'
    # 非居民消极非金融机构，但没有非居民控制人
    CRS103 = 'CRS103'


@unique
class PaymentType(Enum):
    """
    收入类型
    """
    # 股息
    CRS501 = 'CRS501'
    # 利息
    CRS502 = 'CRS502'
    # 销售或者赎回金融资产总收入
    CRS503 = 'CRS503'
    # 其他
    CRS504 = 'CRS504'


@unique
class NameType(Enum):
    """
    姓名类型
    """
    # 个人姓名
    OECD202 = 'OECD202'
    # 别名
    OECD203 = 'OECD203'
    # 昵称
    OECD204 = 'OECD204'
    # 亦称作(aka)
    OECD205 = 'OECD205'
    # 出生姓名
    OECD208 = 'OECD208'


@unique
class AddressType(Enum):
    """
    地址类型
    """
    # 居住地址或办公地址
    OECD301 = 'OECD301'
    # 居住地址
    OECD302 = 'OECD302'
    # 办公地址
    OECD303 = 'OECD303'
    # 注册地址
    OECD304 = 'OECD304'
    # 其他
    OECD305 = 'OECD305'


class MessageHeader(BaseObject):
    """
    消息头
    """
    # 系统用户账号
    ReportingID = None
    # 金融机构注册码（固定长度14位）
    FIID = None
    # 保送类型：固定为CRS
    ReportingType = "CRS"
    # 报告唯一编码，与报告文件名相同。
    # 不得重复，不可复用
    MessageRefId = None
    # 所报送数据所属公立年度，每个报告应仅包含一个年度的数据。
    # 报送期内只能报送前一公立年度的数据。
    # 格式 YYYY-12-31
    ReportingPeriod = None
    # 报告类型（固定长度6位）
    MessageTypeIndic = None
    # 报告生成时间戳（可以和文件名不一致）
    # 格式示例：2018-03-26T10:00:13
    Tmstp = None


@unique
class DocType(Enum):
    """
    账户报告类型定义类
    """
    # 新账户记录
    R1 = 'R1'
    # 修改账户记录
    R2 = 'R2'
    # 删除账户记录
    R3 = 'R3'
    # 测试新账户记录
    T1 = 'T1'
    # 测试修改账户记录
    T2 = 'T2'
    # 测试删除账户记录
    T3 = 'T3'


class DocSpec:
    """
    账户报告文档描述
    """
    # 账户记录编号，不得重复（固定长度29位）
    # 格式：CN+4位年份信息+14位金融机构注册码+9位数字序列号
    # 例如：CN2017C1YINUFUXUEZCI000000001
    # 注意：年份信息和消息头的年度必须一致！
    DocRefId = None
    # 被修改或被删除的账户记录编号（固定长度29位）
    # 新数据报告不得包括此字段
    CorrDocRefId = None
    # 账户报告的类型（固定长度2位）
    DocTypeIndic = None


class MoneyAmnt:
    """
    货币金额
    """
    # 货币代码（固定3位大写英文字母）
    # 取值参考ISO 4217
    # 常见值：USD/美元、HKD/港元、CNY/人名币等
    currCode = None
    # 金额(小数点后保留两位数字)
    amount = 0.00


class Payment:
    """
    账户收入
    """
    # 收入类型
    PaymentType = None
    # 收入金额
    PaymentAmnt = None


class AccountReport:
    """
    账户报告
    """
    # 账户报告文档描述
    DocSpec = None
    # 账号或具有账号类似功能的相关代码（最大长度100）
    AccountNumber = None
    # 账户是否也已经注销（true或false）
    #   true ：账户已注销
    #   false：正常户
    # 注意：2017年7月1日之前消户的无需报送。
    ClosedAccount = "false"
    # 账户类别，按实际开户时间填写（P或N）
    #   N：新开账户
    #   P：存量账户
    # 参考《非居民金融账户涉税信息尽职调查管理办法》第十五条
    """
    存量账户是指符合下列条件之一的账户，包括存量个人账户和存量机构账户：
    （一）截至2017年6月30日由金融机构保有的、由个人或者机构持有的金融账户；
    （二）2017年7月1日（含当日，下同）以后开立并同时符合下列条件的金融账户：
        1.账户持有人已在同一金融机构开立了本款第一项所述账户的；
        2.上述金融机构在确定账户加总余额时将本款第二项所述账户与本款第一项所述账户视为同一账户的；
        3.金融机构已经对本款第一项所述账户进行反洗钱客户身份识别的；
        4.账户开立时，账户持有人无需提供除本办法要求以外的其他信息的。
    存量个人账户包括低净值账户和高净值账户，
    低净值账户是指截至2017年6月30日账户加总余额不超过相当于一百万美元（简称“一百万美元”，下同）的账户，
    高净值账户是指截至2017年6月30日账户加总余额超过一百万美元的账户。
    新开账户是指2017年7月1日以后在金融机构开立的，除第二款第二项规定账户外，
    由个人或者机构持有的金融账户，包括新开个人账户和新开机构账户。
    """
    DueDiligenceInd = None
    # 是否取得账户持有人的自证声明（true或false）
    SelfCertification = "false"
    # 账户余额（必须大于或等于0）
    # 注销账户或实际余额为负时，按0报送
    AccountBalance = None
    # 账户持有人类别（固定长度6位）
    AccountHolderType = None
    # 开户金融机构名称（最大长度200）
    OpeningFIName = None
    # 账户收入
    Payment = None
    # 账户持有人信息
    AccountHolder = None
    # 控制人信息
    # 账户持有人类型为CRS101时必填，否则不得填报
    #   CRS101 ：有非居民控制人的消极非金融机构
    ControllingPerson = None


class AccountHolder:
    """
    账户持有人信息
    当账户持有人类型为CRS100时，有且仅有个人账户持有人信息。
    当账户持有人类型为CRS100以外时，有且仅有机构账户持有人信息。
    """
    # 个人账户持有人信息
    Individual = None
    # 机构账户持有人信息
    Organisation = None


class NamePerson:
    """
    个人姓名
    """
    # 姓名类型(NameType)
    nameType = None
    # 英文(拼音)姓. (最大长度100)
    # 身份证件只有中文的,填写拼音
    # 法定姓名为单名时,填于此处
    FirstName = None
    # 英文中间名(最大长度100)
    MiddleName = None
    # 英文(拼音)名.(最大长度100)
    # 身份证件只有中文的,填写拼音
    # 法定姓名为单名时,固定填"NFN"
    LastName = None
    # 中文姓名
    # 开户证件有中文姓名的应填报
    NameCN = None
    # 前置标题
    # 可选,最大200
    PreceedingTitle = None
    # 头衔(如 : Mr,Dr,Ms,Herr)
    # 可选,最大200
    Title = None
    # 前缀(如: de, van, von)
    # 可选,最大200
    NamePrefix = None
    # 世代标识(如: Jnr, Third)
    # 可选,最大200
    GenerationIdentifier = None
    # 可选,最大200
    # 后缀(如: PhD, VC, QC)
    Suffix = None
    # 一般后缀(如: Deceased, Retired)
    # 可选,最大200
    GeneralSuffix = None


class Individual:
    """
    个人账户持有人信息
    """
    # 姓名(NamePerson)
    Name = None
    # 性别(M/F/N)
    #   M:男, F:女, N:未说明
    Gender = None
    # 地址()
    Address = None


class Addess:
    """
    地址信息
    所有账户必须填报英文地址及其国家代码,位于中国境内的地址(国家代码CN),
    如有中文地址应填报.
    """
    # 地址类型(AddressType)
    legalAddressType = None
    # 国家代码(固定长度2位)
    # ISO 3166
    CountryCode = None

# < stc: CountryCode > CH < / stc: CountryCode >
# < stc: AddressEN >
# < stc: AddressFixEN >
# < stc: CityEN > Acc
# City < / stc: CityEN >
# < stc: Street > Acc
# Street < / stc: Street >
# < stc: BuildingIdentifier > Acc
# Building
# Identifier < / stc: BuildingIdentifier >
# < stc: SuiteIdentifier > Acc
# Suite
# ID < / stc: SuiteIdentifier >
# < stc: FloorIdentifier > Acc
# FloorIdentifier < / stc: FloorIdentifier >
# < stc: DistrictName > Acc
# District < / stc: DistrictName >
# < stc: POB > Acc
# POB < / stc: POB >
# < stc: PostCode > Acc
# PostCode < / stc: PostCode >
# < stc: CountrySubentity > Acc
# CountrySubentity < / stc: CountrySubentity >
# < / stc: AddressFixEN >
# < stc: AddressFreeEN > 123
# Street
# Name / City / State < / stc: AddressFreeEN >
# < / stc: AddressEN >
# < stc: AddressCN >
# < stc: AddressFixCN >
# < stc: CityCN > 110000 < / stc: CityCN >
# < stc: DistrictName > 110108 < / stc: DistrictName >
# < stc: PostCode > 110000 < / stc: PostCode >
# < stc: Province > 110000 < / stc: Province >
# < / stc: AddressFixCN >
# < stc: AddressFreeCN > AddressFreeCN4 < / stc: AddressFreeCN >
# < / stc: AddressCN >
# < / stc: Address >
# < stc: PhoneNo > 123459 < / stc: PhoneNo >
# < stc: IDType > ACC220 < / stc: IDType >
# < stc: IDNumber > 1237 < / stc: IDNumber >
# < stc: ResCountryCode > CH < / stc: ResCountryCode >
# < stc: ResCountryCode > HK < / stc: ResCountryCode >
# < stc: ResCountryCode > US < / stc: ResCountryCode >
# < stc: ResCountryCode > GB < / stc: ResCountryCode >
# < stc: TIN
# issuedBy = "CH"
# inType = "TIN" > 123546 < / stc: TIN >
# < stc: TIN
# issuedBy = "US"
# inType = "TIN" > 164666 < / stc: TIN >
# < stc: TIN
# issuedBy = "GB"
# inType = "TIN" > 151653 < / stc: TIN >
# < stc: TIN
# issuedBy = "HK"
# inType = "TIN" > 16343 < / stc: TIN >
# < stc: Nationality > JP < / stc: Nationality >
# < stc: BirthInfo >
# < stc: BirthDate > 1980 - 02 - 26 < / stc: BirthDate >
# < stc: CountryInfo >
# < stc: CountryCode > DE < / stc: CountryCode >
# < / stc: CountryInfo >
# < / stc: BirthInfo >
# < / cncrs: Individual >

header = MessageHeader()
logcm.print_obj(header, "header")
