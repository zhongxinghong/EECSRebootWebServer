#!/usr/bin/env python3
# -*- coding: utf-8
# filename: root.py

from flask import Blueprint, jsonify


bpOnline = Blueprint('online', __name__)


@bpOnline.route('/', methods=['GET'])
def root():
    return "Hello Online !"