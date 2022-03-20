# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2022/3/15 下午9:22
# software: PyCharm
from cone.communication import DingRobot

robots = [
    DingRobot(name='裘一', token='deca7812002f387023c9cc04b77d0a8c9ed1a4f703f19cd16e431806edb8c9bd', secret='SEC1692e6f5ba22183a6c9cc41a38bbb8e03a5537c90fb6a867b7e34f9ed27ad0f3'),
    DingRobot(name='不上', token='18b48b2ddf7e13944fafb4a25f3129e50b70bd8f44e6b4704b5e93799f618505', secret='SEC551cb984408051fb0544bbca1c21b6c14abd5da9fd1f0c197ce1408f65e40858')
]


for robot in robots:
    robot.send_msg(content="Hello, I am %s" % robot.name)

