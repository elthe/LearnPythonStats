# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Wechat common api
微信相关共通函数
"""

from common import logcm

import requests
import json

'''
基础环境：微信通知
'''


class EnterpriseMessage():
    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid

    def Token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        # corpid,corpsecret 为微信端获取
        params = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret
        }
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        r = requests.get(url=url, params=params)
        token = json.loads(r.text)['access_token']
        logcm.print_obj(token, "token")

        return token

    def send_txt(self, target_type, target_id, text):
        data = {
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": text
            },
            "safe": 0
        }
        # 根据目标类型，设置参数数据
        if target_type == "user":
            data["touser"] = target_id

        elif target_type == "party":
            data["toparty"] = target_id

        elif target_type == "tag":
            data["totag"] = target_id

        # json.dumps在解析格式时，会使用ascii字符集，所以解析后的数据无法显示中文，ensure_ascii不解析为ascii字符集，使用原有字符集
        value = json.dumps(data, ensure_ascii=False)
        token = self.Token()
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % (token)
        r = requests.post(url, data=value)
        return r.text


if __name__ == '__main__':
    s = EnterpriseMessage("你好，欢迎")
    s.send_txt('user', '', '')
