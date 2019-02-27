#!/usr/bin/env python3
# -*- coding: utf-8
# filename: onsite.py

from flask import Blueprint, jsonify, request
from ..core.models import db, OnlineOrder, OnsiteOrder
from ..core.hooks import verify_timestamp, verify_signature, required_login
from ..core.parser import get_str_field
from ..core.models import db, OnlineOrder, OnsiteOrder
from ..core.const import OnsiteOrderStatus
from ..core.exceptions import OK, ServerException, UnknownException, OnlineOrderNotFoundError,\
    OnsiteOrderNotFoundError, NotWaitingStatusError
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


@bpOnsite.route('/stat_status')
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
    try:
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

    except ServerException as e:
        return jsonify(e.to_dict())
    except Exception as e:
        return jsonify(UnknownException(e).to_dict())
    else:
        return jsonify(OK({
                "activityid": ACTIVITY.id,
                "status": stat,
            }).to_dict())


@bpOnsite.route('/current_position', methods=['POST'])
@verify_signature
@required_login
@verify_timestamp
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
    try:
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

    except ServerException as e:
        return jsonify(e.to_dict())
    except Exception as e:
        return jsonify(UnknownException(e).to_dict())
    else:
        return jsonify(OK({
                "position": pos,
            }).to_dict())


@bpOnsite.route('/create', methods=['POST'])
@verify_signature
@required_login
@verify_timestamp
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
    try:
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

    except ServerException as e:
        return jsonify(e.to_dict())
    except Exception as e:
        return jsonify(UnknownException(e).to_dict())
    else:
        return jsonify(OK({
                "onsiteid": order.id,
                "position": pos,
            }).to_dict())
