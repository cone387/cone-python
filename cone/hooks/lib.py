# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2022/3/18 下午10:29
# software: PyCharm
import sys
from typing import Union


__all__ = [
    'hook_model_object'
]


def pop_sys_module(package, target_module):
    packages = {}
    t = None
    for k, v in sys.modules.items():
        if getattr(v, '__package__', None) == package:
            packages[k] = v
            if k == target_module:
                t = v
    for k in packages:
        sys.modules.pop(k)
    assert t is not None, '%s is not found in sys.modules' % target_module
    return t


def hook_model_object(source_obj: Union[object, str], target_obj):
    import importlib
    import inspect

    # get main.py stack
    frames = inspect.stack()
    frames.reverse()
    global_objects = frames[-2].frame.f_globals

    if type(source_obj) is str:
        module_str, obj_name = source_obj.rsplit('.', 1)
        module = importlib.import_module(module_str)
        source_obj = getattr(module, obj_name)
    obj_name = source_obj.__name__
    module_str = source_obj.__module__
    package = module_str.split('.')[0]
    sys_module = pop_sys_module(package, module_str)
    setattr(sys_module, obj_name, target_obj)
    sys.modules[module_str] = sys_module

    # global_objects = globals()
    module_parent, module_name = module_str.rsplit('.', 1)
    parent = importlib.import_module(module_parent)
    setattr(parent, module_name, sys_module)
    #
    for k, v in global_objects.items():
        if getattr(v, '__package__', None) == package:
            global_objects[k] = sys.modules[v.__name__]


