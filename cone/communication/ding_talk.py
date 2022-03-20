# -*- coding: utf-8 -*-
"""
File Name:    ding_talk
Author:       Cone
Date:         2022/3/15
"""

import requests
import time
import hmac
import hashlib
import base64
import urllib.parse
import urllib
import random

url = 'https://oapi.dingtalk.com/robot/send'


class DingRobot:

    def __init__(self, name, token, secret):
        self.name = name
        self.token = token
        self.secret = secret

    def get_sign_timestamp(self):
        timestamp = str(round(time.time() * 1000))
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        hmac_code = hmac.new(self.secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign, timestamp

    def send_msg(self, content=None, msg_type="text"):
        # 每个机器人每分钟最多发送20条消息到群里，如果超过20条，会限流10分钟。
        sign, timestamp = self.get_sign_timestamp()
        data = {
            "msgtype": msg_type,
            msg_type: {"content": content}
        }
        params = {
            "access_token": self.token,
            "timestamp": timestamp,
            "sign": sign
        }
        response = requests.post(url, params=params, json=data)
        assert response.json()['errcode'] == 0, response.json()['errmsg']
        print("[%s]send message success, message is %s" % (self.name, data['text']))

    def __str__(self):
        return self.name

    __repr__ = __str__
