# -*- coding: utf-8 -*-
"""
File Name:    pattern
Author:       Cone
Date:         2022/3/15
"""

from cone import patterns



@patterns.instance(1, b=2, c=3)
class E(metaclass=patterns.SingletonMeta):
    def __init__(self, a, b, c=1):
        self.a = a
        print(f"I'm instance of A({a}, {b}, c={c})")


@patterns.instance
class F(patterns.Singleton):
    def __init__(self):
        self.c = 13
        print("I'm instance of B()")



@patterns.singleton
class A:
    pass


class B(patterns.Singleton):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        print(a, b)

class C(metaclass=patterns.SingletonMeta):
    def __init__(self, c):
        self.a = c
        print(c)

if __name__ == '__main__':

    # print(A() == A())
    # print(B(a=1, b=2) == B(a=3, b=2))
    # print(C(c='c') == C(c='d'))

    # print(E.a)
    # F

    def dd(a, *, c):
        print(a,  c)

    dd(1, b=1, c=1)
    print('')

