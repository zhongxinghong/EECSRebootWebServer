#!/usr/bin/env python3
# -*- coding: utf-8
# filename: online.py

from flask import Blueprint, jsonify, request
from ..core.models import db, OnlineOrder
from ..core.parser import get_str_field, get_int_field
from ..core.hooks import verify_timestamp, verify_signature, required_login
from ..core.const import REPAIR_TYPES, OnlineOrderStatus
from ..core.exceptions import ServerException, OK, UnknownException, RepeatedOnlineOrderError,\
    OnlineOrderNotFoundError, HasOnsiteOrderError
from .activity import _get_latest_activity


bpOnline = Blueprint('online', __name__)


@bpOnline.route('/stat_periods')
def stat_periods():
    """
    获得当次活动现场已预约的数量

    :Method   GET
    :Return {
        "activityid": 2,
        "status": {
            "07:30-08:00": 1,
            "09:30-09:50": 1
        }
    }
    """
    try:
        ACTIVITY, PERIODS = _get_latest_activity()
        res = db.session.query(OnlineOrder.period, db.func.count())\
                        .filter_by(
                            activity_id = ACTIVITY.id,
                            status = OnlineOrderStatus.VALID,
                        )\
                       .group_by(OnlineOrder.period)\
                       .all()
    except ServerException as e:
        return jsonify(e.to_dict())
    except Exception as e:
        return jsonify(UnknownException(e).to_dict())
    else:
        return jsonify(OK({
                "activityid": ACTIVITY.id,
                "status": dict(res),
            }).to_dict())


@bpOnline.route('/create', methods=['POST'])
@verify_signature
@required_login
@verify_timestamp
def create_order():
    """
    创建网上预约订单

    :Method   POST
    :Form
        - userid      str   用户id
        - timestamp   int   毫秒时间戳
        - signature   str   表单签名
        - model       str   电脑类型
        - type        str   问题类型，可选 ('dust','hardware','software','other')
        - desc        str   问题描述（可空，返回空字符串）
        - period      str   预约时段，需返回 periods 列表中的值
    :Return
        - orderid     int   订单id
    :Raise
        - RepeatedOnlineOrderError   注：这将返回已有的 orderid
    """
    try:
        ACTIVITY, PERIODS = _get_latest_activity()

        data = request.form
        userid = data["userid"] # 已经校验过
        timestamp = int(data['timestamp']) // 1000
        model = get_str_field("model", data)
        type_ = get_str_field("type", data, REPAIR_TYPES)
        desc = get_str_field("desc", data)
        period = get_str_field("period", data, PERIODS)

        order = OnlineOrder(userid, ACTIVITY.id, period, model, type_, desc, timestamp)
        o = OnlineOrder.query.filter_by(
                user_id = order.user_id,
                activity_id = order.activity_id,
                status = OnlineOrderStatus.VALID,
            ).scalar()
        if o is None:
            db.session.add(order)
            db.session.commit()
        else:
            raise RepeatedOnlineOrderError(o.id)

    except ServerException as e:
        return jsonify(e.to_dict())
    except Exception as e:
        return jsonify(UnknownException(e).to_dict())
    else:
        return jsonify(OK({
                "orderid": order.id,
            }).to_dict())


@bpOnline.route('/get', methods=['POST'])
@verify_signature
@required_login
@verify_timestamp
def get_order():
    """
    查询订单

    :Method   POST
    :Form
        - userid      str   用户id
        - timestamp   int   毫秒时间戳
        - signature   str   表单签名
    :Return {
        'activityid': 1,
        'date': '2018-10-20',
        'desc': '测试啦哈哈哈1551258704457',
        'end': '17:00',
        'model': 'ThinkPad X230',
        'orderid': 1,
        'period': '15:00-15:30',
        'site': '二教 410',
        'start': '14:00',
        'status': 0,
        'type': 'hardware'
    }
    :Raise
        - OnlineOrderNotFoundError
    """
    try:
        ACTIVITY, PERIODS = _get_latest_activity()

        data = request.form
        userid = data["userid"]

        order = OnlineOrder.query.filter_by(
                user_id = userid,
                activity_id = ACTIVITY.id,
                status = OnlineOrderStatus.VALID,
            ).scalar()

        if order is None:
            raise OnlineOrderNotFoundError()

    except ServerException as e:
        return jsonify(e.to_dict())
    except Exception as e:
        return jsonify(UnknownException(e).to_dict())
    else:
        return jsonify(OK({
                "orderid": order.id,
                "status": order.status,
                "activityid": order.activity.id,
                "date": order.activity.date,
                "site": order.activity.site,
                "start": order.activity.start,
                "end": order.activity.end,
                "model": order.model,
                "type": order.type,
                "desc": order.desc,
                "period": order.period,
            }).to_dict())


@bpOnline.route("/withdraw", methods=['POST'])
@verify_signature
@required_login
@verify_timestamp
def withdraw_order():
    """
    撤回线上预约订单
    注：已经在现场挂过号的线上订单不可撤回

    :Method   POST
    :Form
        - userid      str   用户id
        - orderid     int   网上订单的 id
        - timestamp   int   毫秒时间戳
        - signature   str   表单签名
    :Return
        - orderid     int   网上订单的 id
        - status      int
    :Raise
        - OnlineOrderNotFoundError
        - HasOnsiteOrderError
    """
    try:
        ACTIVITY, PERIODS = _get_latest_activity()

        data = request.form
        userid = data["userid"]
        orderid = get_int_field("orderid")

        order = OnlineOrder.query.filter_by(
                id = orderid,
                user_id = userid,
                activity_id = ACTIVITY.id,
                status = OnlineOrderStatus.VALID,
            ).scalar()

        if order is None:
            raise OnlineOrderNotFoundError()

        o = order.onsite.scalar()
        if o is not None: # 已经在现场挂过号的订单不可撤回
            raise HasOnsiteOrderError(order.id, o.id)

        order.status = OnlineOrderStatus.WITHDRAW.value # 更新的时候一定要加上 .value 否则无法提交
        db.session.commit()

    except ServerException as e:
        return jsonify(e.to_dict())
    except Exception as e:
        return jsonify(UnknownException(e).to_dict())
    else:
        return jsonify(OK({
                "orderid": order.id,
                "status": order.status,
            }).to_dict())

