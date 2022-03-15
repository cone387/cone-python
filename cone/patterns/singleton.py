# -*- coding: utf-8 -*-
"""
File Name:    singleton
Author:       Cone
Date:         2022/3/15
"""

_instances = {}


def _get_instance(cls, *args, **kwargs):
    global _instances
    if cls not in _instances:
        _instances[cls] = object.__new__(cls)
    instance = _instances[cls]
    if args or kwargs:
        instance.__init__(*args, **kwargs)
    return instance


def singleton(cls):
    def inner():
        return _get_instance(cls)
    return inner


class SingletonMeta(type):
    def __call__(cls, *args, **kwargs):
        return _get_instance(cls, *args, **kwargs)


class Singleton(metaclass=SingletonMeta):

    def __call__(self, *args, **kwargs):
        return _get_instance(self.__class__, *args, **kwargs)
