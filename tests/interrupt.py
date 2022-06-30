# -*- coding: utf-8 -*-
"""
File Name:    signal
Author:       Cone
Date:         2022/3/21
"""


from cone.hooks import signal



def on_interrupt(signum, frame):
    print(signum, frame)
    exit(0)


signal.on_sys_interrupt(on_interrupt)

# while True:
#     import time
#     time.sleep(1)
#





class MysqlItemPipeline():
    pass


class SqlitePipeline():
    pass


class CSVPipline():
    pass


class JsonRecorder():
    pass