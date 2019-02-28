#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: hooks.py

__all__ = [

    "verify_timestamp",
    "verify_signature",

    "required_login",
    "required_admin",
    "required_invitation",

    ]


import time
from functools import wraps
from flask import request
from .models import User, Admin
from .wrapper import hook_wrapper
from .parser import get_int_field, get_str_field
from .safety import get_signature, get_admin_auth, get_invitation_auth
from .const import MAX_TIMESTAMP_DELAY, MAX_ADMIN_ID_LENGTH
from .exceptions import InvalidTimestampError, LoginStateError, InvalidSignatureError,\
    AuthorizationTypeError, InvalidAuthorizationCodeError, AdminNotFoundError, AdminIDTooLongError


def _filter_fields(data, exclude=[]):
    assert isinstance(exclude, (list,tuple,set))
    return {k:v for k,v in data.items() if k not in exclude}


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

        s0 = get_signature(_filter_fields(data, ["signature",]))
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

    :Raise
        - AdminNotFoundError
        - AuthorizationTypeError
        - InvalidAuthorizationCodeError
    """
    @wraps(func)
    @hook_wrapper
    def wrapper(*args, **kwargs):

        data = request.form or request.args

        adminid = get_str_field("adminid", data)
        if len(adminid) > MAX_ADMIN_ID_LENGTH:
            raise AdminIDTooLongError(adminid, MAX_ADMIN_ID_LENGTH)

        admin = Admin.query.get(adminid)
        if admin is None:
            raise AdminNotFoundError(adminid)

        auth = get_str_field("authorization", data)
        type_, code = auth.split()
        if type_.lower() != "Administrator".lower():
            raise AuthorizationTypeError(type_)

        s0 = get_admin_auth(_filter_fields(data, ["authorization","signature"]), admin.password)

        if code != s0:
            raise InvalidAuthorizationCodeError(type_, code)

        return func(*args, **kwargs)
    return wrapper


def required_invitation(func):
    """
    需要邀请码

    :Raise
        - AuthorizationTypeError
        - InvalidAuthorizationCodeError
    """
    @wraps(func)
    @hook_wrapper
    def wrapper(*args, **kwargs):

        data = request.form or request.args
        auth = get_str_field("authorization", data)

        type_, code = auth.split()

        if type_.lower() != "Invitation".lower():
            raise AuthorizationTypeError(type_)

        s0 = get_invitation_auth(_filter_fields(data, ["authorization","signature"]))
        if code != s0:
            raise InvalidAuthorizationCodeError(type_, code)

        return func(*args, **kwargs)
    return wrapper