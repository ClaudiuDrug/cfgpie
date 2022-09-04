# -*- coding: UTF-8 -*-

from sys import modules
from types import ModuleType
from weakref import WeakValueDictionary

MODULE: ModuleType = modules.get("__main__")
INSTANCES = WeakValueDictionary()
