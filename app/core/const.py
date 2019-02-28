#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: const.py

__all__ = [

    "ROOT_DIR", "BASE_DIR",

    "MAX_ADMIN_ID_LENGTH",
    "MAX_TIMESTAMP_DELAY",
    "ACTIVITY_PERIOD_SPAN",
    "REPAIR_TYPES",

    "OnlineOrderStatus", "OnsiteOrderStatus",

    ]


from enum import IntEnum, unique
from .utils import _absP


ROOT_DIR = _absP("../") # project dir
BASE_DIR = _absP("./")  # app dir

MAX_ADMIN_ID_LENGTH = 128
MAX_TIMESTAMP_DELAY = 30 * 1000 # 30s
ACTIVITY_PERIOD_SPAN = 30
REPAIR_TYPES = ('dust','hardware','software','other')

""" Status Enum 在某些场合需要调 .value 属性转为真正的 int 值 ！ """

@unique
class OnlineOrderStatus(IntEnum):
    VALID    = 0
    WITHDRAW = 1
    INVALID  = 2

@unique
class OnsiteOrderStatus(IntEnum):
    WAITING    = 0
    PROCESSING = 1
    FINISHED   = 2
