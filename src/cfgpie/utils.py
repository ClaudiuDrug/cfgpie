# -*- coding: UTF-8 -*-

from os import makedirs
from os.path import dirname, realpath, exists


def ensure_folder(path: str):
    """
    Read the file path and recursively create the folder structure if needed.
    """
    folder_path: str = dirname(realpath(path))

    if not exists(path):
        make_dirs(folder_path)


def make_dirs(path: str):
    """Checks if a folder path exists and create one if not."""
    try:
        makedirs(path)
    except FileExistsError:
        pass


def folder(value: str) -> str:
    """
    Return `value` as path and recursively
    create the folder structure if needed.
    """
    value: str = realpath(value)
    make_dirs(value)
    return value


def file(value: str) -> str:
    """
    Return `value` as path and recursively
    create the folder structure if needed.
    """
    value: str = realpath(value)
    ensure_folder(value)
    return value
