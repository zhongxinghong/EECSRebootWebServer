#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: safety.py

__all__ = [

    "bMD5", "bSHA1", "bSHA256",
    "xMD5", "xSHA1", "xSHA256",

    "bHMAC_MD5", "bHMAC_SHA1", "bHMAC_SHA256",
    "xHMAC_MD5", "xHMAC_SHA1", "xHMAC_SHA256",

    "get_admin_password",

    "_get_raw_signature_string",
    "get_signature",

    "get_invitation_auth"
    "get_admin_auth",

    ]


import hashlib
import hmac
from .utils import b, u
from .secret import ADMIN_PASSWORD_SALT, INVITATION_CODE


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

def bHMAC_MD5(k, s):
    return hmac.new(b(k), b(s), hashlib.md5).digest()

def bHMAC_SHA1(k, s):
    return hmac.new(b(k), b(s), hashlib.sha1).digest()

def bHMAC_SHA256(k, s):
    return hmac.new(b(k), b(s), hashlib.sha256).digest()

def xHMAC_MD5(k, s):
    return hmac.new(b(k), b(s), hashlib.md5).hexdigest()

def xHMAC_SHA1(k, s):
    return hmac.new(b(k), b(s), hashlib.sha1).hexdigest()

def xHMAC_SHA256(k, s):
    return hmac.new(b(k), b(s), hashlib.sha256).hexdigest()


def get_admin_password(userid):
    return xMD5(userid + ADMIN_PASSWORD_SALT)


def _get_raw_signature_string(data):
    return "".join("&%s=%s" % (k, v) for k, v in sorted(data.items()))

def get_signature(data):
    return xMD5(_get_raw_signature_string(data))


def get_invitation_auth(data):
    return xHMAC_MD5(INVITATION_CODE, _get_raw_signature_string(data))

def get_admin_auth(data, password):
    return xHMAC_MD5(password, _get_raw_signature_string(data))
