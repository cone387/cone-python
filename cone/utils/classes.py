import os
import sys
import pathlib
import importlib
import inspect
from typing import Union

WORKING_DIR = os.getcwd()
WORKING_DIR_SPLIT = WORKING_DIR.split(os.sep)


class ClassManager(dict):
    _mapping = {}

    @staticmethod
    def to_path_list(path):
        if isinstance(path, pathlib.Path):
            path [path]
        elif isinstance(path, str):
            path = path.split(',')
        assert isinstance(path, list), "path must be list of string, but got %s" % type(path)
        return path

    def __new__(cls, path=None, **kwargs):
        path = cls.to_path_list(path)
        key = ",".join(path) or kwargs.pop('name', None)
        assert key, "path or name must be provided"
        if key not in cls._mapping:
            cls._mapping[key] = super(ClassManager, cls).__new__(cls)
        return cls._mapping[key]

    def __init__(self, *, path=None, unique_keys=None):
        super(ClassManager, self).__init__()
        assert unique_keys and isinstance(unique_keys, (str, list, tuple)), \
            "unique_keys must be string or list of string, but got %s" % type(unique_keys)
        path = self.to_path_list(path)
        self.path = [os.path.abspath(os.path.join(os.getcwd(), x)) for x in path] if path else []
        if isinstance(unique_keys, str):
            unique_keys = [unique_keys]
        self.unique_keys = unique_keys
        self._loaded = False

    def _is_manageable_class(self, cls):
        return getattr(cls, '__manager__', None) == self

    @staticmethod
    def _is_manageable_file(file: pathlib.Path):
        return file.suffix.endswith('py') and (not file.stem.startswith('_'))

    @staticmethod
    def find_common_prefix(path1, path2):
        for i in range(min(len(path1), len(path2))):
            if path1[i] != path2[i]:
                return path1[:i]
        return path1[:min(len(path1), len(path2))]

    @staticmethod
    def _load_class(file: pathlib.Path):
        # assert work_dir in str(file), "file %s is not in work_dir %s" % (file, work_dir)
        module_path_split = ClassManager.find_common_prefix(WORKING_DIR_SPLIT, str(file).split(os.sep))
        module_path = None
        while module_path_split:
            module_path = os.sep.join(module_path_split)
            if module_path in sys.path:
                break
            module_path_split.pop()
        assert module_path, "file %s is not in work_dir %s" % (file, WORKING_DIR)
        module = file.relative_to(module_path).with_suffix('').as_posix().replace('/', '.')
        importlib.import_module(module)

    def _load_classes(self, path_or_file: Union[str, pathlib.Path]):
        if isinstance(path_or_file, str):
            path_or_file = pathlib.Path(path_or_file)
        if path_or_file.is_dir():
            for p in path_or_file.glob('*'):
                try:
                    self._load_classes(p)
                except ImportError:
                    pass
        elif path_or_file.is_file() and self._is_manageable_file(path_or_file):
            self._load_class(path_or_file)

    def __call__(self, *, is_registry=True, generator=None, overwritable=False, **kwargs):
        is_registry = is_registry or generator is not None
        if is_registry:
            for k, v in kwargs.items():
                if k not in self.unique_keys:
                    is_registry = False
                    break
        if not is_registry:
            cls = self.find(**kwargs)
            args = inspect.getfullargspec(cls).args
            for k in self.unique_keys:
                if k not in args:
                    kwargs.pop(k)
            return cls(**kwargs)
        else:
            return self.register(generator=generator, overwritable=overwritable, **kwargs)

    def register(self, generator=None, overwritable=False, **kwargs):
        def wrapper(cls):
            if generator:
                assert callable(generator), "generator must be callable"
                for keys in generator():
                    if isinstance(keys, str):
                        keys = [keys]
                    self._add_class(cls, overwritable=overwritable, generated=True,
                                    **dict(zip(self.unique_keys, keys)))
            else:
                self._add_class(cls, **kwargs)
            return cls

        return wrapper

    def register_from(self, path):
        if self._loaded:
            self._load_classes(path)
        else:
            self.path.append(path)

    def _gen_key(self, **kwargs):
        if len(self.unique_keys) == 1:
            return kwargs[self.unique_keys[0]]
        return tuple(kwargs[key] for key in self.unique_keys)

    def _add_class(self, cls, overwritable=False, generated=False, **kwargs):
        unique_key = self._gen_key(**kwargs)
        exists = super(ClassManager, self).get(unique_key, None)
        if exists and not getattr(exists, '__overwritable__', False):
            raise KeyError("class %s already exists and is not overwritable" % unique_key)
        setattr(cls, '__overwritable__', overwritable)
        setattr(cls, '__manager__', self)
        if generated:
            setattr(cls, '__generated__', True)
            setattr(cls, '__generated_args__', kwargs)
        else:
            for key, value in kwargs.items():
                if key in self.unique_keys:
                    setattr(cls, key, value)
        self[unique_key] = cls

    def _ensure_loaded(self):
        if not self._loaded:
            for path in self.path:
                self._load_classes(path)
            self._loaded = True

    def __getitem__(self, key):
        self._ensure_loaded()
        return super(ClassManager, self).__getitem__(key)

    def __iter__(self):
        self._ensure_loaded()
        return super(ClassManager, self).__iter__()

    def keys(self):
        self._ensure_loaded()
        return super(ClassManager, self).keys()

    def values(self):
        self._ensure_loaded()
        return super(ClassManager, self).values()

    def items(self):
        self._ensure_loaded()
        return super(ClassManager, self).items()

    def get(self, key, default=None):
        try:
            cls = self[key]
            if getattr(cls, '__generated__', False):
                for key, value in getattr(cls, '__generated_args__', {}).items():
                    if key in self.unique_keys:
                        setattr(cls, key, value)
            return cls
        except KeyError:
            return default

    def find(self, **kwargs):
        return self.get(self._gen_key(**kwargs))

    def __str__(self):
        return "ClassManager(path=%s, num=%s)" % (self.path, len(self))
