#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: hooks.py

__all__ = [

    "verify_timestamp",
    "verify_signature",

    "required_login",
    "required_admin",

    ]


import time
from functools import wraps
from flask import request
from .models import User
from .wrapper import hook_wrapper
from .parser import get_int_field, get_str_field
from .safety import get_signature
from .const import MAX_TIMESTAMP_DELAY
from .exceptions import InvalidTimestampError, LoginStateError, InvalidSignatureError


def verify_timestamp(func):
    """
    检查 timestamp 合理性

    :Raise
        - InvalidTimestampError
    """
    @wraps(func)
    @hook_wrapper
    def wrapper(*args, **kwargs):

        t0 = get_int_field("timestamp")
        t1 = int(time.time() * 1000)
        delta = t1 - t0
        if delta >= MAX_TIMESTAMP_DELAY:
            raise InvalidTimestampError(t0)

        return func(*args, **kwargs)
    return wrapper


def verify_signature(func):
    """
    检查 signature 合理性

    :Raise
        - InvalidSignatureError
    """
    @wraps(func)
    @hook_wrapper
    def wrapper(*args, **kwargs):

        data = request.form or request.args
        signature = get_str_field("signature", data)
        s0 = get_signature({k:v for k,v in data.items() if k != "signature"})
        if signature != s0:
            raise InvalidSignatureError(signature)

        return func(*args, **kwargs)
    return wrapper


def required_login(func):
    """
    检查用户是否登录

    :Raise
        - LoginStateError
    """
    @wraps(func)
    @hook_wrapper
    def wrapper(*args, **kwargs):

        userid = get_str_field("userid")
        if User.query.get(userid) is None:
            raise LoginStateError(userid)

        return func(*args, **kwargs)
    return wrapper


def required_admin(func):
    """
    需要管理员权限
    """
    @wraps(func)
    @hook_wrapper
    def wrapper(*args, **kwargs):

        return func(*args, **kwargs)
    return wrapper

