# -*- coding: utf-8 -*-
"""
File Name:    exception
Author:       Cone
Date:         2022/3/15
"""
import sys

sys_excepthook = sys.excepthook


def setSysExceptHook(onExcept):
    def _sys_excepthook(excType, excValue, tb):
        sys_excepthook(excType, excValue, tb)
        onExcept(excType, excValue, tb)
    sys.excepthook = _sys_excepthook
