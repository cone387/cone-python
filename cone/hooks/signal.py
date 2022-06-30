# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2022/3/20 下午4:26
# software: PyCharm

import signal


def on_sys_interrupt(func):
    signal.signal(signal.SIGTERM, func)
    signal.signal(signal.SIGINT, func)



