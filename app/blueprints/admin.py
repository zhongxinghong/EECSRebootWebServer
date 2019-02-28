#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: admin.py

from flask import Blueprint, request
from ..core.wrapper import api_view_wrapper
from ..core.hooks import verify_timestamp, verify_signature, required_admin


bpAdmin = Blueprint('admin', __name__)

