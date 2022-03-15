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

    def send_msg(self):
        # 每个机器人每分钟最多发送20条消息到群里，如果超过20条，会限流10分钟。
        sign, timestamp = self.get_sign_timestamp()
        data = {
            "msgtype": "text",
            "text": {"content": "我就是"}
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


Robots = [
    Robot(name='裘一', token='deca7812002f387023c9cc04b77d0a8c9ed1a4f703f19cd16e431806edb8c9bd', secret='SEC1692e6f5ba22183a6c9cc41a38bbb8e03a5537c90fb6a867b7e34f9ed27ad0f3'),
    Robot(name='不上', token='18b48b2ddf7e13944fafb4a25f3129e50b70bd8f44e6b4704b5e93799f618505', secret='SEC551cb984408051fb0544bbca1c21b6c14abd5da9fd1f0c197ce1408f65e40858')
]


robot = random.choice(Robots)
robot.send_msg()

