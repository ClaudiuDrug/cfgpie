# -*- coding: UTF-8 -*-

from os import makedirs
from os.path import dirname, realpath, exists

__all__ = [
    "ensure_folder",
    "folder",
    "file",
]


def ensure_folder(path: str):
    """
    Read the file path and recursively create the folder structure if needed.
    """
    folder_path: str = dirname(realpath(path))
    if not exists(folder_path):
        make_dirs(folder_path)


def make_dirs(path: str):
    """Recursively create the folder structure."""
    try:
        makedirs(path)
    except FileExistsError:
        pass


def folder(path: str) -> str:
    """
    Return `value` as path and recursively
    create the folder structure if needed.
    """
    path: str = realpath(path)
    if not exists(path):
        make_dirs(path)
    return path


def file(path: str) -> str:
    """
    Return `value` as path and recursively
    create the folder structure if needed.
    """
    path: str = realpath(path)
    ensure_folder(path)
    return path
