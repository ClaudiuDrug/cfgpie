# -*- coding: UTF-8 -*-

from .constants import INSTANCES
from .handlers import CfgParser


def get_config(name: str = "cfgpie", **kwargs) -> CfgParser:
    if name not in INSTANCES:
        # a strong reference is required
        instance: CfgParser = CfgParser(name, **kwargs)
        INSTANCES[name] = instance
    return INSTANCES[name]


__all__ = ["CfgParser", "get_config"]
