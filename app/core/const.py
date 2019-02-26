#!/usr/bin/env python3
# -*- coding: utf-8
# filename: const.py

__all__ = [

    "ROOT_DIR", "BASE_DIR",

    "MAX_TIMESTAMP_DELAY",

    "OnlineOrderStatus", "OnsiteOrderStatus",

    ]


from enum import IntEnum, unique
from .utils import _absP


ROOT_DIR = _absP("../") # project dir
BASE_DIR = _absP("./")  # app dir

MAX_TIMESTAMP_DELAY = 30 * 1000 # 30s

@unique
class OnlineOrderStatus(IntEnum):
    VALID    = 0
    WITHDRAW = 1
    INVALID  = 2

@unique
class OnsiteOrderStatus(IntEnum):
    Waiting    = 0
    Processing = 1
    Finished   = 2