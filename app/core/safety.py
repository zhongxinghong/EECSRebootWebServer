#!/usr/bin/env python3
# -*- coding: utf-8
# filename: safety.py

__all__ = [

    "bMD5", "bSHA1", "bSHA256",
    "xMD5", "xSHA1", "xSHA256",

    "_get_pre_signature_string",
    "get_signature",

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


def _get_pre_signature_string(data):
    return "&".join("=".join( (k, str(v)) ) for k, v in sorted(data.items()))

def get_signature(data):
    return xMD5(_get_pre_signature_string(data))
