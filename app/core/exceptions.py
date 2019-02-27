#!/usr/bin/env python3
# -*- coding: utf-8
# filename: exceptions.py

__all__ = [

"EECSRebootException",

    "ServerException",
        "OK",
        "UnknownException",
        "FormKeyMissingError",
        "FormValueTypeError",
        "FormValueOutOfRangeError",
        "FormValueFormatError",
        "InvalidTimestampError",
        "LoginStateError",
        "InvalidSignatureError",
        "RepeatedActivityError",
        "RepeatedOnlineOrderError",
        "OnlineOrderNotFoundError",
        "OnsiteOrderNotFoundError",
        "NotWaitingStatusError",
        "HasOnsiteOrderError",

    ]


import time
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

class FormValueTypeError(ServerException):
    """ 表单值类型错误 """
    code = 102
    desc = "Some form values are typed incorrectly"

    def __init__(self, key, value, type_):
        detail = {
            "key": key,
            "value": value,
            "required": type_.__name__,
        }
        super().__init__(detail)

class FormValueOutOfRangeError(ServerException):
    """ 表单值超出限制范围 """
    code = 103
    desc = "Some form values are out of range"

    def __init__(self, key, value, limited):
        detail = {
            "key": key,
            "value": value,
            "limited": limited,
        }
        super().__init__(detail)

class FormValueFormatError(ServerException):
    """ 表单值的格式错误 """
    code = 104
    desc = "Some form values are not formatted correctly"

    def __init__(self, key, value, regex):
        detail = {
            "key": key,
            "value": value,
            "required": regex.pattern,
        }
        super().__init__(detail)

class InvalidTimestampError(ServerException):
    """ 无效的时间戳 """
    code = 201
    desc = "Timestamp is invalid"

    def __init__(self, timestamp):
        detail = {"invalid": timestamp}
        super().__init__(detail)

class LoginStateError(ServerException):
    """ 登录态异常 """
    code = 202
    desc = "Required login"

    def __init__(self, userid):
        detail = {"userid": userid}
        super().__init__(detail)

class InvalidSignatureError(ServerException):
    """ 无效的签名字段 """
    code = 203
    desc = "Signature is invalid"

    def __init__(self, signature):
        detail = {"invalid": signature}
        super().__init__(detail)

class RepeatedActivityError(ServerException):
    """ 活动重复创建 """
    code = 301
    desc = "Create Repeated activity"

    def __init__(self, activity):
        detail = {
            "date": activity.date,
            "site": activity.site,
            "start": activity.start,
            "end": activity.end,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(activity.timestamp))),
        }
        super().__init__(detail)

class RepeatedOnlineOrderError(ServerException):
    """ 单次活动线上重复预约 """
    code = 401
    desc = "One activity, one valid online order for one user"

    def __init__(self, orderid):
        detail = {"orderid": orderid}
        super().__init__(detail)

class OnlineOrderNotFoundError(ServerException):
    """ 当次活动未存在有效的线上预约订单 """
    code = 402
    desc = "No valid online order"

class OnsiteOrderNotFoundError(ServerException):
    """ 当次活动未存在有效的现场维修订单 """
    code = 403
    desc = "No valid onsite order"

class NotWaitingStatusError(ServerException):
    """ 试图查询一个非 WAITING 状态现场订单的队列位置 """
    code = 404
    desc = "Order status is not WAITING"

    def __init__(self, orderid, status):
        detail = {
            "orderid": orderid,
            "status": status, # 当前状态
        }
        super().__init__(detail)

class HasOnsiteOrderError(ServerException):
    """ 线上订单已经在线下预约成功，此时不可再更改 """
    code = 405
    desc = "The online order associated to a onsite order is immutable"

    def __init__(self, onlineid, onsiteid):
        detail = {
            "onlineid": onlineid,
            "onsiteid": onsiteid,
        }
        super().__init__(detail)