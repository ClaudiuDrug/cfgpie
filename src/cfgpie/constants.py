# -*- coding: UTF-8 -*-

from os.path import dirname, realpath, abspath, join
from sys import modules, argv
from types import ModuleType
from weakref import WeakValueDictionary

__all__ = [
    "NAME", "INSTANCES", "RLOCKS", "ROOT", "CONFIG"
]

# default instance name:
NAME: str = "cfgpie"

# config parser instances container:
INSTANCES: WeakValueDictionary = WeakValueDictionary()

# recursive thread locks container:
RLOCKS: WeakValueDictionary = WeakValueDictionary()

# main python module:
MODULE: ModuleType = modules.get("__main__")

# root directory:
try:
    # Try to access '__file__' attribute
    ROOT: str = realpath(dirname(MODULE.__file__))
except AttributeError:
    # Fallback: Use the current working directory or script path from argv
    ROOT: str = realpath(dirname(abspath(argv[0])))

# config default file path:
CONFIG: str = join(ROOT, "config", "config.ini")
