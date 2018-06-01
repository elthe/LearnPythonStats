from common.classcm import BaseObject
from common import datecm
from common import dictcm


class Module(BaseObject):
    """
    模块
    """

    def __init__(self, packageName, moduleName, moduleDesc):
        """

        :param packageName:
        :param moduleName:
        :param moduleDesc:
        """
        self.packageName = packageName
        self.moduleName = moduleName
        self.moduleDesc = moduleDesc
        self.codeCreateTime = datecm.now_time_str("%Y年%m月%d日 00:00:00")
        self.services = []
        self.beans = []
        self.codes = []


class Service(BaseObject):
    """
    接口
    """

    def __init__(self, svc):
        self.interfaceName = svc["Service"]["interfaceName"]
        self.startVersion = svc["Service"]["startVersion"]
        self.desc = svc["Service"]["desc"]
        self.interfaceName = svc["Service"]["interfaceName"]
        self.reqProps = []
        for req in svc["subItems"]["req"]:
            self.reqProps.append(Prop(**req))
        self.respProps = []
        for resp in svc["subItems"]["resp"]:
            self.respProps.append(Prop(**resp))

        self.methodName = self.interfaceName.split(".")[0]
        self.hasReqData = len(self.reqProps) > 0


class Prop(BaseObject):
    """
    属性
    """

    def __init__(self, **kwargs):
        """
        属性初始化
        :param kwargs:
        """
        self.name = dictcm.get(kwargs, "name")
        self.type = dictcm.get(kwargs, "type")
        self.id = dictcm.get(kwargs, "id")
        self.startVersion = dictcm.get(kwargs, "startVersion")
        self.desc = dictcm.get(kwargs, "desc")
