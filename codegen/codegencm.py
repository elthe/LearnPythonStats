from common.classcm import BaseObject


class Module(BaseObject):
    """
    模块
    """
    pass


class Service(BaseObject):
    """
    接口
    """
    req = []
    resp = []
    pass


class Prop(BaseObject):
    """
    属性
    """

    def __init__(self, name, remark, **kwargs):
        self.name = name
        self.remark = remark

