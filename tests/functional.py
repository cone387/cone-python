# -*- coding: utf-8 -*-
"""
File Name:    functional
Author:       Cone
Date:         2022/3/15
"""

from cone.utils.functional import cached_property, classproperty
from cone.utils import functional

class A:
    b = 1

    @cached_property
    def a(self):
        return self.b + 1

    @classproperty
    def c(cls):
        return cls.b + 4

class B:
    _a = 1

    @cached_property
    def a(self):
        return self._a + 2

a = A()
print(a.a)
print(a.a)

b = B()
print(b.a)
print(b.a)

print(A.c)
print(A().c)
import re

def _lazy_re_compile(regex, flags=0):
    """Lazily compile a regex with flags."""

    def _compile():
        # Compile the regex if it was not passed pre-compiled.
        if isinstance(regex, (str, bytes)):
            return re.compile(regex, flags)
        else:
            assert not flags, "flags must be empty if regex is passed pre-compiled"
            return regex

    return functional.SimpleLazyObject(_compile)


# a = functional.lazystr('dasdd')
# print(a)

a = _lazy_re_compile('redasd')

a.search('dasd')