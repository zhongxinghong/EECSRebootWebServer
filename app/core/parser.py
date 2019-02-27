#!/usr/bin/env python3
# -*- coding: utf-8
# filename: parser.py

__all_ = [

    "get_int_field",
    "get_float_field",
    "get_str_field",

    ]


from flask import request
from .exceptions import FormKeyMissingError, FormValueTypeError, FormValueOutOfRangeError,\
    FormValueFormatError


def _get_field(type_, key, data=None, limited=None, regex=None):
    """
    获取特定类型表单值的函数的模板
    对表单值做通用的合理性校验

    :Raise
        - FormKeyMissingError
        - FormValueTypeError
        - FormValueOutOfRangeError
    """
    if data is None:
        data = request.form or request.args
    value = data.get(key)
    if value is None:
        raise FormKeyMissingError(key)
    try:
        value = type_(value)
    except ValueError:
        raise FormValueTypeError(key, value, type_)
    if limited is not None and value not in limited:
        raise FormValueOutOfRangeError(key, value, limited)
    if regex is not None and regex.match(value) is None:
        raise FormValueFormatError(key, value, regex)
    return value


def get_str_field(key, data=None, limited=None, regex=None):
    return _get_field(str, key, data=data, limited=limited, regex=regex)

def get_int_field(key, data=None, limited=None):
    return _get_field(int, key, data=data, limited=limited)

def get_float_field(key, data=None, limited=None):
    return _get_field(float, key, data=data, limited=limited)

