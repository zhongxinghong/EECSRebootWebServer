#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: root.py

import time
from flask import Blueprint, redirect, url_for, request
from ..core.wrapper import api_view_wrapper
from ..core.parser import get_str_field
from ..core.safety import _get_pre_signature_string, get_signature


bpRoot = Blueprint('root', __name__)


@bpRoot.route('/')
def root():
    return "Hello World !"

@bpRoot.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename="assets/favicon.ico"))

@bpRoot.route('/robots.txt')
def robots_txt():
    return redirect(url_for('static', filename="robots.txt"))

@bpRoot.route('/get_timestamp')
@api_view_wrapper
def get_timestamp():
    """
    返回服务器时间

    :Method   GET
    :Return   float   秒时间戳
    """
    return {
        "timestamp": time.time(),
    }

@bpRoot.route('/test_signature', methods=['GET','POST'])
@api_view_wrapper
def test_signature():
    """
    检查 signature 生成方式是否正确
    """
    data = request.form or request.args
    formSign = get_str_field("signature", data)
    data = {k:v for k,v in data.items() if k != "signature"}
    preString = _get_pre_signature_string(data)
    targetSign = get_signature(data)

    return {
        "current": formSign,
        "target": targetSign,
        "presign": preString,
        "valid": (formSign == targetSign),
    }

