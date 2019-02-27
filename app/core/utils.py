#!/usr/bin/env python3
# -*- coding: utf-8
# filename: utils.py

__all__ = [

    "regex_activity_date",
    "regex_activity_time",
    "regex_activity_period",

    "_absP",
    "_mkdir",

    "b", "u",

    ]


import os
import re


regex_activity_date = re.compile(r'^\d{4}-\d{2}-\d{2}$')
regex_activity_time = re.compile(r'^\d{2}:\d{2}$')
regex_activity_period = re.compile(r'^\d{2}:\d{2}-\d{2}:\d{2}$')


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
