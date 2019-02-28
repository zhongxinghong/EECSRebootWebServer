#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: wrapper.py

__all__ = [

    "api_view_wrapper",
    "hook_wrapper"

    ]


from functools import wraps
from flask import jsonify
from .exceptions import OK, ServerException, UnknownException


def api_view_wrapper(func):
    """
    api view 函数的外壳
    提供模板化的错误捕获和标准返回
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        func -- 视图函数，要求返回值为 detail 字典
        """
        try:
            res = func(*args, **kwargs)
        except ServerException as e:
            return jsonify(e.to_dict())
        except Exception as e:
            return jsonify(UnknownException(e).to_dict())
        else:
            return jsonify(OK(res).to_dict())
    return wrapper


def hook_wrapper(func):
    """
    hook 修饰器内 wrapper 函数的外壳
    提供模板化的错误捕获和标准返回
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except ServerException as e:
            return jsonify(e.to_dict())
        except Exception as e:
            return jsonify(UnknownException(e).to_dict())
        else:
            return res
    return wrapper
