#!/usr/bin/env python3
# -*- coding: utf-8
# filename: root.py

import time
from flask import Blueprint, redirect, url_for, jsonify
from ..core.exceptions import OK


bpRoot = Blueprint('root', __name__)


@bpRoot.route('/', methods=['GET'])
def root():
    return "Hello World !"

@bpRoot.route('/favicon.ico', methods=["GET"])
def favicon():
    return redirect(url_for('static', filename="assets/favicon.ico"))

@bpRoot.route('/robots.txt', methods=['GET'])
def robots_txt():
    return redirect(url_for('static', filename="robots.txt"))

@bpRoot.route('/get_timestamp', methods=['GET'])
def get_timestamp():
    """
    返回服务器时间

    :Method   GET
    :Return   float   秒时间戳
    """
    return jsonify(OK({
            "timestamp": time.time(),
        }).to_dict())
