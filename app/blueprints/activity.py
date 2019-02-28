#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: activity.py

import datetime
from flask import Blueprint, request
from ..core.models import db, Activity
from ..core.wrapper import api_view_wrapper
from ..core.hooks import verify_timestamp, verify_signature, required_admin
from ..core.parser import get_str_field
from ..core.utils import regex_activity_date, regex_activity_time
from ..core.const import ACTIVITY_PERIOD_SPAN
from ..core.exceptions import RepeatedActivityError


bpActivity = Blueprint('activity', __name__)


def _get_periods(start, end, span):
    """ 生成预约时段选项 """
    pClock = lambda clockStr: datetime.datetime.strptime(clockStr, "%H:%M") # 会自动添零
    fClock = lambda clockObj: datetime.datetime.strftime(clockObj, "%H:%M")

    start, end = map(pClock, (start, end))
    span = datetime.timedelta(minutes=span)

    periods = []
    now = start
    while True:
        if now + span < end:
            periods.append("{}-{}".format(fClock(now), fClock(now + span)))
            now += span
        else:
            periods.append("{}-{}".format(fClock(now), fClock(end)))
            break

    return periods


def _get_latest_activity():
    """ 获得当前活动 """
    _latestDate = db.session.query(db.func.max(Activity.date)).scalar()
    ACTIVITY = Activity.query.filter(Activity.date == _latestDate).scalar()
    PERIODS = _get_periods(ACTIVITY.start, ACTIVITY.end, ACTIVITY_PERIOD_SPAN)
    return (ACTIVITY, PERIODS)


@bpActivity.route('/create', methods=['POST'])
@verify_timestamp
@required_admin
@verify_signature
@api_view_wrapper
def create_activity():
    """
    创建一个活动

    :Method   POST
    :Form
        - adminid     str       管理员id
        - timestamp   int       毫秒时间戳
        - signature   str       表单签名
        - date        char[10]  活动时间，格式 yyyy-mm-dd ，确保长度为 10
        - site        str       活动地点
        - start       char[5]   活动开始时间，格式 HH:MM ，确保长度为 5
        - end         char[5]   活动结束时间，格式 HH:MM ，确保长度为 5
    :Return
        - acitvityid   int   活动id
    :Raise
        - RepeatedActivityError
    """
    data = request.form
    timestamp = int(data['timestamp']) // 1000
    date = get_str_field("date", data=data, regex=regex_activity_date)
    site = get_str_field("site", data)
    start = get_str_field("start", data=data, regex=regex_activity_time)
    end = get_str_field("end", data=data, regex=regex_activity_time)

    activity = Activity(date, site, start, end, timestamp)
    a = Activity.query.filter(Activity.date == date).scalar()
    if a is None:
        db.session.add(activity)
        db.session.commit()
    else:
        raise RepeatedActivityError(a)

    return {
        "activityid": activity.id,
    }


@bpActivity.route('/get_latest')
@api_view_wrapper
def get_latest_activity():
    """
    获得最近的活动信息

    :Method   GET
    :Return {
        "date": "2018-10-20",
        "site": "二教 410",
        "start": "14:00",
        "end": "17:00",
        "periods": [
          "14:00-14:30",
          "14:30-15:00",
          "15:00-15:30",
          "15:30-16:00",
          "16:00-16:30",
          "16:30-17:00"
        ]
    }
    """
    ACTIVITY, PERIODS = _get_latest_activity()

    return {
        "date": ACTIVITY.date,
        "site": ACTIVITY.site,
        "start": ACTIVITY.start,
        "end": ACTIVITY.end,
        "periods": PERIODS,
    }

