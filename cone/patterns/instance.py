# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2020-01-10 17:19
# software: PyCharm
from inspect import isclass


def instance(*args, **kwargs):
    def params_instance(cls):
        return cls(*args, **kwargs)  # 带参数的实例
    if args and isclass(args[0]):
        # bug: function args[0] cant be a class type
        return args[0]()
    return params_instance

