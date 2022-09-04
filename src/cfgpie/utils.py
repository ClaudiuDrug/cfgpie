# -*- coding: UTF-8 -*-

from ast import literal_eval
from os import makedirs
from os.path import dirname, realpath, exists, isdir
from typing import Any


def ensure_folder(path: str):
    """
    Read the file path and recursively create the folder structure if needed.
    """
    folder_path: str = dirname(realpath(path))
    try:
        make_dirs(folder_path)
    except FileExistsError:
        pass


def make_dirs(path: str):
    """Checks if a folder path exists and create one if not."""
    if (not exists(path)) and (not isdir(path)):
        makedirs(path)


def evaluate(value: str) -> Any:
    """Transform a string to an appropriate data type."""
    try:
        return literal_eval(value)
    except (SyntaxError, ValueError):
        raise
