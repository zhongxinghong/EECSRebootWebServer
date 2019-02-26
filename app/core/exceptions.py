#!/usr/bin/env python3
# -*- coding: utf-8
# filename: exceptions.py

__all__ = [

"EECSRebootException",

    "ServerException",
        "OK",
        "UnknownException",
        "FormKeyMissingError",
        "InvalidTimestampError",

    ]


from flask import jsonify


class EECSRebootException(Exception):
    """ 项目异常类的抽象基类 """


class ServerException(EECSRebootException):
    """ 服务器异常类的抽象基类 """
    code = None
    desc = ""

    def __init__(self, detail=None, msg=None):
        if self.__class__ is __class__:
            raise NotImplementedError
        self.detail = detail
        self.msg = msg or self.__class__.desc

    def to_dict(self):
        return {
            "errcode": self.__class__.code,
            "errmsg": self.msg,
            "detail": self.detail,
        }


class OK(ServerException):
    """ 正常 """
    code = 0
    desc = "Success"

    def __init__(self, data):
        super().__init__(data)


class UnknownException(ServerException):
    """ 未知错误 """
    code = -1
    desc = "Unknown exception"

    def __init__(self, err):
        detail = {"error": repr(err)}
        super().__init__(detail)


class FormKeyMissingError(ServerException):
    """ 表单键缺失 """
    code = 101
    desc = "Some form keys are missing"

    def __init__(self, *required):
        if len(required) == 0:
            detail = None
        elif len(required) == 1:
            detail = {"required": required[0]}
        else:
            detail = {"required": required}
        super().__init__(detail)


class InvalidTimestampError(ServerException):
    """ 无效的时间戳 """
    code = 201
    desc = "Timestamp is invalid"

    def __init__(self, timestamp):
        detail = {"invalid": timestamp}
        super().__init__(detail)