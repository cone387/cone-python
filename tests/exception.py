# -*- coding: utf-8 -*-
"""
File Name:    exception
Author:       Cone
Date:         2022/3/15
"""

from cone.communication import ding_talk
from cone.hooks import exception

def a(*args):
    ding_talk.DingRobot(
        name='裘一',
        token='deca7812002f387023c9cc04b77d0a8c9ed1a4f703f19cd16e431806edb8c9bd',
        secret='SEC1692e6f5ba22183a6c9cc41a38bbb8e03a5537c90fb6a867b7e34f9ed27ad0f3'
    ).send_msg("args is %s" % str(args))

exception.setSysExceptHook(a)

1/0