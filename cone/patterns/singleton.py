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
    def __call__(cls, **kwargs):
        return _get_instance(cls, **kwargs)


class Singleton(metaclass=SingletonMeta):
    pass

    # def __new__(cls, *args, **kwargs):
    #     return _get_instance(cls, **kwargs)


if __name__ == '__main__':
    @singleton
    class A:
        pass

    class B(Singleton):
        def __init__(self, a, b):
            self.a = a
            self.b = b
            print(a, b)

    class C(metaclass=SingletonMeta):
        def __init__(self, c):
            self.a = c
            print(c)

    print(A() == A())
    print(B(a=1, b=2) == B(a=3, b=2))
    print(C(c='c') == C(c='d'))
    print(_instances)