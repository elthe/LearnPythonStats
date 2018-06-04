from common.classcm import BaseObject
from common import datecm
from common import strcm

"""
代码生成相关的模块相关类定义
"""


class Module(BaseObject):
    """
    模块
    """

    def __init__(self, **kwargs):
        """
        模块初始化
        """
        # 模块包名
        self.packageName = ""
        # 模块名
        self.moduleName = ""
        # 模块描述
        self.moduleDesc = ""

        self.copy_from(kwargs)

        # 模块创建时间
        self.codeCreateTime = datecm.now_time_str("%Y年%m月%d日 00:00:00")
        # 模块名首字母大写
        self.moduleNameFcu = strcm.upper_first(self.moduleName)
        # 常量KEY名
        self.keyName = strcm.camel_to_under(self.moduleName).upper()
        # 接口列表
        self.services = []
        # Bean列表
        self.beans = []
        # Code列表
        self.codes = []


class Service(BaseObject):
    """
    接口
    """

    def __init__(self, svc):
        """
        接口初始化
        :param svc:接口定义字典
        """
        # 接口名
        self.interfaceName = ""
        # 开始版本
        self.startVersion = ""
        # 接口描述
        self.desc = ""

        # 属性复制
        if svc is not None and "Service" in svc:
            self.copy_from(svc["Service"])

        # 其他属性初始化
        # 方法名
        self.methodName = self.interfaceName.split(".")[0]
        # 类名
        self.className = strcm.upper_first(self.methodName)

        # 请求参数属性列表
        self.reqProps = []
        # 请求参数读取
        for req in svc["subItems"]["req"]:
            self.reqProps.append(Prop(**req))
        # 是否包含请求参数
        self.hasReqData = len(self.reqProps) > 0

        # 返回参数属性列表
        self.respProps = []
        # 返回参数读取
        for resp in svc["subItems"]["resp"]:
            self.respProps.append(Prop(**resp))


class Bean(BaseObject):
    """
    Bean
    """

    def __init__(self, bean):
        """
        Bean初始化
        :param bean:bean定义字典
        """

        # 名称
        self.name = ""
        # 描述
        self.desc = ""
        # 类名
        self.className = ""
        # 开始版本
        self.startVersion = ""

        # 属性复制
        if bean is not None and "Bean" in bean:
            self.copy_from(bean["Bean"])

        # 父类名
        self.superClassName = ""
        # 是否有父类
        self.hasSuperClass = False
        # 是否有数值属性
        self.hasBigDecimalProp = True
        # 是否有日期属性
        self.hasDateProp = True
        # 是否有列表属性
        self.hasListProp = True
        # 属性列表
        self.props = []
        # 请求参数读取
        for prop in bean["subItems"]["prop"]:
            self.props.append(Prop(**prop))
        # Bean列表
        self.beans = []


class Prop(BaseObject):
    """
    属性
    """

    def __init__(self, **kwargs):
        """
        属性初始化
        :param kwargs:
        """
        # 属性名
        self.name = ""
        # 属性类型
        self.type = ""
        # 属性ID
        self.id = ""
        # 开始版本
        self.startVersion = ""
        # 描述
        self.desc = ""
        # 是否可以为空
        self.nullable = ""
        # 默认值
        self.defaultVal = ""

        self.copy_from(kwargs)

        # 首字母大写的ID
        self.idFcu = strcm.upper_first(self.id)
        # 是否包含Bean
        self.hasBean = False
        # Bean
        self.bean = ""
        # 是否列表
        self.isList = False


class Code(BaseObject):
    """
    Code
    """

    def __init__(self, code):
        """
        Code初始化
        :param code:code定义字典
        """

        # Code名
        self.name = ""
        # Code的KEY
        self.key = ""
        # Code描述
        self.desc = ""
        # 开始版本
        self.startVersion = ""

        # 属性复制
        if code is not None and "Code" in code:
            self.copy_from(code["Code"])

        # 选项列表
        self.options = []
        # 选项读取
        for option in code["subItems"]["option"]:
            self.options.append(Option(**option))


class Option(BaseObject):
    """
    选项
    """

    def __init__(self, **kwargs):
        """
        属性初始化
        :param kwargs:
        """

        # 选项名
        self.name = ""
        # 选项的Code
        self.code = ""
        # 选项的KEY
        self.key = ""
        # 开始版本
        self.startVersion = ""
        # 描述
        self.desc = ""

        self.copy_from(kwargs)
