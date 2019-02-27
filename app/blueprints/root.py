#!/usr/bin/env python3
# -*- coding: utf-8
# filename: root.py

import time
from flask import Blueprint, redirect, url_for, jsonify, request
from ..core.safety import _get_pre_signature_string, get_signature
from ..core.parser import get_str_field
from ..core.exceptions import OK, ServerException, UnknownException


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
def get_timestamp():
    """
    返回服务器时间

    :Method   GET
    :Return   float   秒时间戳
    """
    return jsonify(OK({
            "timestamp": time.time(),
        }).to_dict())

@bpRoot.route('/test_signature', methods=['GET','POST'])
def test_signature():
    """
    检查 signature 生成方式是否正确
    """
    try:
        data = request.form or request.args
        formSign = get_str_field("signature", data)
        data = {k:v for k,v in data.items() if k != "signature"}
        preString = _get_pre_signature_string(data)
        targetSign = get_signature(data)

    except ServerException as e:
        return jsonify(e.to_dict())
    except Exception as e:
        return jsonify(UnknownException(e).to_dict())
    else:
        return jsonify(OK({
                "current": formSign,
                "target": targetSign,
                "presign": preString,
                "valid": (formSign == targetSign),
            }).to_dict())

