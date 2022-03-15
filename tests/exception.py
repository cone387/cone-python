# -*- coding: utf-8 -*-
"""
File Name:    exception
Author:       Cone
Date:         2022/3/15
"""


from cone.hooks import exception

def a(*args):
    print(args)

exception.setSysExceptHook(a)

1/0