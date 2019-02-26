#!/usr/bin/env python3
# -*- coding: utf-8
# filename: safety.py

__all__ = [

    "bMD5", "bSHA1", "bSHA256",
    "xMD5", "xSHA1", "xSHA256",

    ]


import hashlib
from .utils import b, u


def bMD5(s):
    return hashlib.md5(b(s)).digest()

def bSHA1(s):
    return hashlib.sha1(b(s)).digest()

def bSHA256(s):
    return hashlib.sha256(b(S)).digest()

def xMD5(s):
    return hashlib.md5(b(s)).hexdigest()

def xSHA1(s):
    return hashlib.sha1(b(s)).hexdigest()

def xSHA256(s):
    return hashlib.sha256(b(s)).hexdigest()

