#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: admin.py

from flask import Blueprint, request
from ..core.models import db, Admin
from ..core.wrapper import api_view_wrapper
from ..core.hooks import verify_timestamp, verify_signature, required_admin, required_invitation
from ..core.parser import get_str_field
from ..core.const import MAX_ADMIN_ID_LENGTH
from ..core.exceptions import AdminIDExistedError, AdminNotFoundError, AdminIDTooLongError


bpAdmin = Blueprint('admin', __name__)


@bpAdmin.route('/create', methods=['POST'])
@verify_timestamp
@required_invitation
@verify_signature
@api_view_wrapper
def create():
    """
    创建管理员账号

    :Method   POST
    :Form
        - adminid          str   想要创建的管理员id
        - authorization    str   授权类型 + " " + 授权字段 (type: Invitation)
        - timestamp        int   毫秒时间戳
        - signature        str   表单签名
    :Return
        - adminid          str   用户名
        - password         str   秘钥
    :Raise
        - AdminIDTooLongError
        - AdminIDExistedError
    """
    data = request.form
    adminid = get_str_field("adminid", data)

    if len(adminid) > MAX_ADMIN_ID_LENGTH:
        raise AdminIDTooLongError(adminid, MAX_ADMIN_ID_LENGTH)

    if Admin.query.get(adminid) is not None:
        raise AdminIDExistedError(adminid)

    admin = Admin(adminid)
    db.session.add(admin)
    db.session.commit()

    return {
        "adminid": admin.id,
        "password": admin.password,
    }


'''
@bpAdmin.route('/forgotten_password', methods=['POST'])
@verify_timestamp
@required_invitation
@verify_signature
@api_view_wrapper
def forgotten_password():
    """
    忘记密码后找回（邀请码权限是共享的，因此可以窃取别人的密码）

    :Method   POST
    :Form
        - adminid          str   想要找回密码的管理员id
        - authorization    str   授权类型 + " " + 授权字段 (type: Invitation)
        - timestamp        int   毫秒时间戳
        - signature        str   表单签名
    :Return
        - adminid          str   用户名
        - password         str   秘钥
    :Raise
        - AdminIDTooLongError
        - AdminNotFoundError
    """
    data = request.form
    adminid = get_str_field("adminid", data)

    if len(adminid) > MAX_ADMIN_ID_LENGTH:
        raise AdminIDTooLongError(adminid, MAX_ADMIN_ID_LENGTH)

    admin = Admin.query.get(adminid)

    if admin is None:
        raise AdminNotFoundError(adminid)

    return {
        "adminid": admin.id,
        "password": admin.password,
    }
'''