#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: globals.py

__all__ = [

    "g",

    "cache",

    ]


from flask import g
from flask_caching import Cache

cache = Cache()
