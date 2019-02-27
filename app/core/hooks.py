#!/usr/bin/env python3
# -*- coding: utf-8
# filename: hooks.py

__all__ = [

    "verify_timestamp",
    "verify_signature",

    "required_login",
    "required_admin",

    ]


import time
from functools import wraps
from flask import jsonify, request
from .models import User
from .safety import get_signature
from .parser import get_int_field, get_str_field
from .const import MAX_TIMESTAMP_DELAY
from .exceptions import ServerException, InvalidTimestampError, LoginStateError, InvalidSignatureError


def verify_timestamp(func):
    """
    检查 timestamp 合理性

    :Raise
        - InvalidTimestampError
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            t0 = get_int_field("timestamp")
            t1 = int(time.time() * 1000)
            delta = t1 - t0
            if delta >= MAX_TIMESTAMP_DELAY:
                raise InvalidTimestampError(t0)
        except ServerException as e:
            return jsonify(e.to_dict())
        except Exception as e:
            return jsonify(UnknownException(e).to_dict())
        else:
            return func(*args, **kwargs)
    return wrapper


def verify_signature(func):
    """
    检查 signature 合理性

    :Raise
        - InvalidSignatureError
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = request.form or request.args
            signature = get_str_field("signature", data)
            s0 = get_signature({k:v for k,v in data.items() if k != "signature"})
            if signature != s0:
                raise InvalidSignatureError(signature)
        except ServerException as e:
            return jsonify(e.to_dict())
        except Exception as e:
            return jsonify(UnknownException(e).to_dict())
        else:
            return func(*args, **kwargs)
    return wrapper


def required_login(func):
    """
    检查用户是否登录

    :Raise
        - LoginStateError
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            userid = get_str_field("userid")
            if User.query.get(userid) is None:
                raise LoginStateError(userid)
        except ServerException as e:
            return jsonify(e.to_dict())
        except Exception as e:
            return jsonify(UnknownException(e).to_dict())
        else:
            return func(*args, **kwargs)
    return wrapper


def required_admin(func):
    """
    需要管理员权限
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

