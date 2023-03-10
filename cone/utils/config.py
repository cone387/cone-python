# -*- coding:utf-8 -*-
# author: Cone
# datetime: 2022/11/2 09:42
# software: PyCharm
import os
import argparse

CURRENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config'))
_CONFIG_PATH = []


class ConfigNotFoundError(FileNotFoundError):
    pass


def get_config_path(from_default=True, from_env=True, from_cmd=True, cmd_arg='config-path'):
    global _CONFIG_PATH
    if not _CONFIG_PATH:
        config_path = ''
        if from_env:
            config_path = os.getenv('CONFIG_PATH', '')
        elif from_cmd:
            import argparse
            parser = argparse.ArgumentParser()
            parser.add_argument('--%s' % cmd_arg, type=str, default='')
            args = parser.parse_known_args()[0]
            config_path = args.config_path
        if from_default:
            config_path = config_path + ',' + CURRENT_PATH
        for p in config_path.strip().split(','):
            if p:
                _CONFIG_PATH.append(os.path.abspath(p.strip()))
    return _CONFIG_PATH


class ConfigLoader:

    def __new__(cls, config_file: str, escape=True):
        if config_file.endswith('.json'):
            return JsonConfigLoader(config_file, escape=escape)
        elif config_file.endswith('.yaml'):
            return YamlConfigLoader(config_file, escape=escape)
        elif config_file.endswith('.py'):
            return PythonConfigLoader(config_file, escape=escape)
        raise NotImplementedError

    def __init__(self, config_file, escape=True):
        self.config_file = config_file
        self.escape = escape
        self._content = None
        self._text = None
        self._encoding = 'utf-8'

    @property
    def content(self):
        if not self._content:
            with open(self.config_file, 'rb', encoding=self._encoding) as f:
                self._content = f.read()
        return self._content

    @property
    def text(self):
        if not self._text:
            self._text = self.content.decode(self._encoding)
        return self._text

    def read(self):
        raise NotImplementedError


class JsonConfigLoader(ConfigLoader):

    def read(self):
        import json
        return json.loads(self.content)


class YamlConfigLoader(ConfigLoader):
    def read(self):
        try:
            import yaml
        except ImportError:
            raise ImportError('Please install PyYAML')
        return yaml.load(self.text, Loader=yaml.FullLoader)


class PythonConfigLoader(ConfigLoader):
    def read(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('config', self.config_file)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        return config


def translate_config(config):
    if isinstance(config, dict):
        for k, v in config.copy().items():
            if '-' in k:
                config[k.replace('-', '_')] = v
                del config[k]
            if isinstance(v, dict):
                translate_config(v)
    elif isinstance(config, list):
        for v in config:
            translate_config(v)


def _load_config(name_or_path: str, suffixes=None, escape=True):
    suffixes = suffixes or ['.json']
    with_suffix = name_or_path.split(os.sep)[-1].split('.')[-1] in suffixes
    for p in get_config_path():
        if with_suffix:
            config_file = os.path.join(p, name_or_path)
            if os.path.exists(config_file):
                return ConfigLoader(config_file, escape=escape)
        else:
            for suffix in suffixes:
                config_file = os.path.join(p, '%s%s' % (name_or_path, suffix))
                if os.path.exists(config_file):
                    return ConfigLoader(config_file, escape=escape)
    raise ConfigNotFoundError("config(%s[%s]) not found in %s" % (name_or_path, '|'.join(suffixes), get_config_path()))


def load_config(name_or_path=None, cmd_arg=None, suffixes=None, escape=True):
    assert name_or_path or cmd_arg, "name_or_path or cmd_arg must be set"
    if cmd_arg is not None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--%s' % cmd_arg, type=str)
        args = parser.parse_known_args()[0]
        if args.cmd_arg:
            name_or_path = args.cmd_arg
    return _load_config(name_or_path, suffixes=suffixes, escape=escape)


if __name__ == '__main__':

    load_config('test')