#!/usr/bin/env python3
# -*- coding: utf-8
# filename: user.py

from flask import Blueprint, jsonify, request
from ..core.models import db, User
from ..core.safety import xSHA1
from ..core.hooks import verify_timestamp
from ..core.exceptions import OK, ServerException, UnknownException, FormKeyMissingError


bpUser = Blueprint('user', __name__)


@bpUser.route('/', methods=['GET'])
def root():
    return "Hello User !"

@bpUser.route('/login', methods=['POST'])
@verify_timestamp
def login():
    """
    登录接口

    :Method   POST
    :Form
        - openid      str   小程序用户的 openid 字段
        - timestamp   int   毫秒时间戳
    :Return
        - userid   char[40]   openid 的 sha1.hexdigest 作为 userid
    :Raise
        - FormKeyMissingError
        - InvalidTimestampError
        - UnknownException
    """
    try:
        openid = request.form.get("openid")
        if openid is None:
            raise FormKeyMissingError("openid")
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