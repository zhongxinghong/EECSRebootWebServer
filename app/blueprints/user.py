#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: user.py

from flask import Blueprint, request
from ..core.models import db, User
from ..core.wrapper import api_view_wrapper
from ..core.hooks import verify_timestamp, verify_signature
from ..core.parser import get_str_field


bpUser = Blueprint('user', __name__)


@bpUser.route('/login', methods=['POST'])
@verify_timestamp
@verify_signature
@api_view_wrapper
def login():
    """
    登录接口

    :Method   POST
    :Form
        - openid      str   小程序用户的 openid 字段
        - timestamp   int   毫秒时间戳
        - signature   str   表单签名
    :Return
        - userid   char[40]   openid 的 sha1.hexdigest 作为 userid
    """
    data = request.form
    openid = get_str_field("openid", data)
    user = User(openid)
    userid = user.id
    if User.query.get(userid) is None:
        db.session.add(user)
        db.session.commit()
    return {
        "userid": userid,
    }
