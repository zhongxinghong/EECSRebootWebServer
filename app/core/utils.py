#!/usr/bin/env python3
# -*- coding: utf-8
# filename: utils.py

__all__ = [

    "_absP", "_mkdir",
    "b", "u",

    ]


import os


__basedir = os.path.join(os.path.dirname(__file__), "../") # app root dir

def _absP(*ps):
    return os.path.abspath(os.path.join(__basedir, *ps))

def _mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def b(s):
    """ bytes/str/int/float type to bytes """
    if isinstance(s, bytes):
        return s
    elif isinstance(s, (str, int ,float)):
        return str(s).encode("utf-8")
    else:
        raise TypeError(type(s))

def u(s):
    """ str/int/float/bytes type to utf-8 string """
    if isinstance(s, (str, int, float)):
        return str(s)
    elif isinstance(s, bytes):
        return s.decode("utf-8")
    else:
        raise TypeError(type(s))

