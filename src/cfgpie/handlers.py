# -*- coding: UTF-8 -*-

from ast import literal_eval
from configparser import ConfigParser, ExtendedInterpolation
from decimal import Decimal
from os.path import isfile, exists, realpath
from sys import argv
from threading import RLock
from typing import Iterator, Sequence, Union, List, Dict, Tuple, Any

from .constants import NAME, RLOCKS, ROOT, CONFIG
from .exceptions import ArgParseError
from .utils import ensure_folder, folder, file

__all__ = ["CfgParser"]


class ArgsParser(object):

    @staticmethod
    def _update_params(params: dict, section: str, option: str, value: str):

        if section not in params:
            params.update({section: {option: value}})
        else:
            params.get(section).update({option: value})

    @classmethod
    def parse(cls, args: Iterator[str]) -> dict:
        temp = dict()

        for arg in args:
            if arg.startswith("--") is True:
                stripped = arg.strip("-")
                try:
                    section, option = stripped.split("-")
                except ValueError:
                    raise ArgParseError(f"Inconsistency in cmd-line parameters '{arg}'!")
                else:
                    try:
                        value = next(args)
                    except StopIteration:
                        raise ArgParseError(f"Missing value for parameter '{arg}'")
                    else:
                        if value.startswith("--") is False:
                            cls._update_params(temp, section.upper(), option, value)
                        else:
                            raise ArgParseError(f"Incorrect value '{value}' for parameter '{arg}'!")
            else:
                raise ArgParseError(f"Inconsistency in cmd-line parameters '{arg}'!")

        return temp


class CfgParser(ConfigParser, ArgsParser):
    """Configuration handle."""

    _CONVERTERS: dict = {
        "decimal": Decimal,
        "list": literal_eval,
        "tuple": literal_eval,
        "set": literal_eval,
        "dict": literal_eval,
        "path": realpath,
        "folder": folder,
        "file": file,
    }

    _DEFAULTS: dict = {
        "directory": ROOT,
    }

    @staticmethod
    def _dispatch_rlock(name: str = NAME) -> RLock:
        if name not in RLOCKS:
            instance: RLock = RLock()
            RLOCKS.update({name: instance})
        return RLOCKS.get(name)

    @staticmethod
    def _as_dict(mapping: Union[Dict[str, Any], List[Tuple[str, Any]]] = None, **kwargs) -> dict:
        if mapping is not None:
            kwargs.update(mapping)
        return kwargs

    @staticmethod
    def _exists(item: str) -> bool:
        return exists(item) and isfile(item)

    def __init__(self, name: str = NAME, **kwargs):
        self._name = name

        if "defaults" not in kwargs:
            kwargs.update(defaults=self._DEFAULTS)

        if "interpolation" not in kwargs:
            kwargs.update(interpolation=ExtendedInterpolation())

        if "converters" not in kwargs:
            kwargs.update(converters=self._CONVERTERS)
        else:
            temp: dict = self._CONVERTERS.copy()
            temp.update(kwargs.pop("converters"))
            kwargs.update(converters=temp)

        super(CfgParser, self).__init__(**kwargs)

    @property
    def name(self):
        return self._name

    def parse(self, args: Sequence[str] = None):
        """Parse command-line arguments and update the configuration."""
        with self._thread_lock():
            if args is None:
                args = argv[1:]

            if len(args) > 0:
                self.read_dict(
                    dictionary=super(CfgParser, self).parse(iter(args)),
                    source="<cmd-line>"
                )

    def set_defaults(self, mapping: Union[Dict[str, Any], List[Tuple[str, Any]]] = None, **kwargs):
        """Update `DEFAULT` section with `mapping` & `kwargs`."""
        with self._thread_lock():
            params: dict = self._as_dict(mapping, **kwargs)

            if len(params) > 0:
                self._read_defaults(params)

    def open(self, file_path: Union[str, List[str]], encoding: str = "UTF-8", fallback: dict = None):
        """
        Read from configuration `file_path` which can also be a list of files paths.
        If `file_path` does not exist and `fallback` is provided
        the latter will be used and a new configuration file will be written.
        """
        with self._thread_lock():
            if isinstance(file_path, str):
                file_path = [file_path]

            if any([self._exists(item) for item in file_path]):
                self.read(file_path, encoding=encoding)

            elif fallback is not None:
                self.read_dict(dictionary=fallback, source="<backup>")
                self.save(CONFIG, encoding)

    def save(self, file_path: str, encoding: str = "UTF-8"):
        """Save the configuration to `file_path`."""
        with self._thread_lock():
            ensure_folder(file_path)
            with open(file_path, "w", encoding=encoding) as fh:
                self.write(fh)

    def _thread_lock(self, name: str = NAME) -> RLock:
        if not hasattr(self, "_rlock"):
            self._rlock: RLock = self._dispatch_rlock(name)
        return self._rlock
