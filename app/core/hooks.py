#!/usr/bin/env python3
# -*- coding: utf-8
# filename: hooks.py

__all__ = [

    "verify_timestamp",

    ]


import time
from functools import wraps
from flask import jsonify, request
from .const import MAX_TIMESTAMP_DELAY
from .exceptions import ServerException, InvalidTimestampError


def verify_timestamp(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = request.args or request.form
            t0 = int(data.get("timestamp"))
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