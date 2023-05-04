# -*- coding: UTF-8 -*-

from .constants import NAME, INSTANCES
from .handlers import CfgParser

__all__ = ["CfgParser", "get_config"]


def get_config(name: str = NAME, **kwargs) -> CfgParser:
    if name not in INSTANCES:
        instance: CfgParser = CfgParser(name, **kwargs)
        INSTANCES.update({name: instance})
    return INSTANCES.get(name)
