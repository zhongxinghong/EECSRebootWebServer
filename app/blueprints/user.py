#!/usr/bin/env python3
# -*- coding: utf-8
# filename: user.py

from flask import Blueprint, jsonify, request
from ..core.models import db, User
from ..core.safety import xSHA1
from ..core.parser import get_str_field
from ..core.hooks import verify_timestamp, verify_signature
from ..core.exceptions import OK, ServerException, UnknownException


bpUser = Blueprint('user', __name__)


@bpUser.route('/login', methods=['POST'])
@verify_signature
@verify_timestamp
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
    try:
        data = request.form
        openid = get_str_field("openid", data)
        user = User(openid)
        userid = user.id
        if User.query.get(userid) is None:
            db.session.add(user)
            db.session.commit()
    except ServerException as e:
        return jsonify(e.to_dict())
    except Exception as e:
        return jsonify(UnknownException(e).to_dict())
    else:
        return jsonify(OK({
                "userid": userid,
            }).to_dict())
