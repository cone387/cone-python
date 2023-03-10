# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2022/3/20 下午4:29
# software: PyCharm
import hashlib


def get_md5(string: str):
    m = hashlib.md5()
    m.update(string.encode(encoding='utf-8'))
    return m.hexdigest()