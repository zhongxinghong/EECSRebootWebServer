#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: onsite.py

from flask import Blueprint, request
from ..core.models import db, OnlineOrder, OnsiteOrder
from ..core.wrapper import api_view_wrapper
from ..core.hooks import verify_timestamp, verify_signature, required_login, required_admin
from ..core.parser import get_str_field
from ..core.const import OnsiteOrderStatus
from ..core.exceptions import OnlineOrderNotFoundError, OnsiteOrderNotFoundError, NotWaitingStatusError
from .activity import _get_latest_activity


bpOnsite = Blueprint('onsite', __name__)


def _status_enum_to_map(statusEnum):
    """ 获得 enum 的 value -> key 的映射 """
    return {e.value: e.name.lower() for e in statusEnum}


def _get_current_position(activityid, onsiteid):
    # 需测试！！！
    pos = db.session.query(OnsiteOrder)\
                    .filter(db.and_(
                        OnsiteOrder.status < 2,
                        OnsiteOrder.activity_id == activityid,
                        OnsiteOrder.id < onsiteid, # 只考虑创建时间早于它的订单
                    ))\
                    .count() # 按创建的先后顺序排序
    return pos


@bpOnsite.route('/create', methods=['POST'])
@verify_timestamp
@required_login
@verify_signature
@api_view_wrapper
def create_order():
    """
    创建现场维修订单
    注：重复创建，相当于重复挂号，这将返回已存在的现场维修订单

    :Method   POST
    :Form
        - userid      str   用户id
        - onlineid    int   线上预约订单的id
        - timestamp   int   毫秒时间戳
        - signature   str   表单签名
    :Return
        - onsiteid    int   线下维修订单的id
        - position    int   当前队列位置
    :Raise
        - OnlineOrderNotFoundError
    """
    ACTIVITY, PERIODS = _get_latest_activity()

    data = request.form
    userid = data["userid"]
    timestamp = int(data['timestamp']) // 1000
    onlineID = get_str_field("onlineid", data)

    if OnlineOrder.query.filter_by(
                user_id = userid,
                id = onlineID,
                activity_id = ACTIVITY.id,
            ).scalar() is None:
        raise OnlineOrderNotFoundError()

    order = OnsiteOrder(userid, onlineID, ACTIVITY.id, timestamp)
    o = OnsiteOrder.query.filter_by(
            user_id = order.user_id,
            online_id = order.online_id,
            activity_id = order.activity_id,
        ).scalar()
    if o is None:
        db.session.add(order)
        db.session.commit()
    else:
        order = o # 返回已经创建过的订单

    pos = _get_current_position(ACTIVITY.id, order.id)

    return {
        "onsiteid": order.id,
        "position": pos,
    }


@bpOnsite.route('/stat_status')
@api_view_wrapper
def stat_status():
    """
    获得当次活动的现场维修状态统计

    :Method   GET
    :Return {
        "activityid": 2,
        "status": {
            "waiting": 1,
            "processing": 0,
            "finished": 0
        }
    }
    """
    ACTIVITY, PERIODS = _get_latest_activity()

    res = db.session.query(OnsiteOrder.status, db.func.count())\
                    .filter_by(activity_id=ACTIVITY.id)\
                    .group_by(OnsiteOrder.status)\
                    .all()

    statusMap = _status_enum_to_map(OnsiteOrderStatus)
    stat = dict.fromkeys(statusMap.values(), 0)
    for status, count in res:
        k = statusMap[status]
        stat[k] = count

    return {
        "activityid": ACTIVITY.id,
        "status": stat,
    }


@bpOnsite.route('/current_position', methods=['POST'])
@verify_timestamp
@required_login
@verify_signature
@api_view_wrapper
def current_position():
    """
    获得当前队列位置

    :Method   POST
    :Form
        - userid      str   用户id
        - onsiteid    int   现场维修订单的id
        - timestamp   int   毫秒时间戳
        - signature   str   表单签名
    :Return
        - position    int   当前位置
    :Raise
        - OnsiteOrderNotFoundError
        - NotWaitingStatusError
    """
    ACTIVITY, PERIODS = _get_latest_activity()

    data = request.form
    userid = data["userid"]
    timestamp = int(data['timestamp']) // 1000
    onsiteID = get_str_field("onsiteid", data)

    order = OnsiteOrder.query.filter_by(
                user_id = userid,
                id = onsiteID,
                activity_id = ACTIVITY.id,
            ).scalar()

    if order is None:
        raise OnsiteOrderNotFoundError()

    if order.status != OnsiteOrderStatus.WAITING:
        statusMap = _status_enum_to_map(OnsiteOrderStatus)
        raise NotWaitingStatusError(order, statusMap[order.status])

    pos = _get_current_position(ACTIVITY.id, order.id)

    return {
        "position": pos,
    }


@bpOnsite.route('/queue', methods=['POST'])
@verify_timestamp
@required_admin
@verify_signature
@api_view_wrapper
def get_queue():
    """
    获得现场维修队列

    :Method   POST
    :Form
        - adminid         str   管理员id
        - authorization   str   授权类型 + " " + 授权字段 (type: Administrator)
        - timestamp       int   毫秒时间戳
        - signature       str   表单签名
    :Return {
        'activity': {
            'date': '2018-10-22',
            'end': '09:50',
            'id': 2,
            'site': '二教 410',
            'start': '07:00'
        },
        'orders': [
            {
                'online': {
                    'desc': '测试啦哈哈哈1551266997860',
                    'id': 3,
                    'model': 'ThinkPad X230',
                    'period': '07:30-08:00',
                    'status': 0,
                    'timestamp': 1551266997,
                    'type': 0
                },
                'onsite': {
                    'id': 1,
                    'status': 0,
                    'timestamp': 1551277346
                },
                'userid': 'f3d7323c8b0880976ff2e363e74ab28a6c1c4695'
            },
            .......
        ]
    }
    """
    ACTIVITY, PERIODS = _get_latest_activity()

    res = OnsiteOrder.query.filter_by(activity_id=ACTIVITY.id).all()

    return {
        "activity": {
            "id": ACTIVITY.id,
            "date": ACTIVITY.date,
            "site": ACTIVITY.site,
            "start": ACTIVITY.start,
            "end": ACTIVITY.end,
        },
        "orders": [{
            "userid": o.user_id,
            "onsite": {
                "id": o.id,
                "status": o.status,
                "timestamp": o.timestamp,
            },
            "online": {
                "id": o.online_id,
                "model": o.online.model,
                "period": o.online.period,
                "status": o.online.status,
                "type": o.online.status,
                "desc": o.online.desc,
                "timestamp": o.online.timestamp,
            }
        } for o in res],
    }