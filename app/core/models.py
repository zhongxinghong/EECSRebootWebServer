#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: models.py

__all__ = [

    "db",

    "User",
    "Admin",
    "Activity",
    "OnlineOrder",
    "OnsiteOrder",

    ]


import time
from flask_sqlalchemy import SQLAlchemy
from .utils import regex_activity_date, regex_activity_time, regex_activity_period
from .const import MAX_ADMIN_ID_LENGTH, OnsiteOrderStatus, OnlineOrderStatus
from .safety import xSHA1, get_admin_password


db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "user"

    id     = db.Column(db.String(40), primary_key=True)
    openid = db.Column(db.Text, nullable=False)
    online = db.relationship('OnlineOrder', backref='user', lazy='dynamic')
    onsite = db.relationship('OnsiteOrder', backref='user', lazy='dynamic')

    def __init__(self, openID):
        self.id = xSHA1(openID)
        self.openid = openID

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.id)


class Admin(db.Model):

    __tablename__ = "admin"

    id       = db.Column(db.String(MAX_ADMIN_ID_LENGTH), primary_key=True)
    password = db.Column(db.String(32), nullable=False)

    def __init__(self, adminID):
        assert len(adminID) <= MAX_ADMIN_ID_LENGTH
        password = get_admin_password(adminID)
        assert len(password) == 32
        self.id = adminID
        self.password = password

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.id)


class Activity(db.Model):

    __tablename__ = "activity"


    id        = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    date      = db.Column(db.String(10), nullable=False)   # 活动日期
    site      = db.Column(db.Text, nullable=False)         # 活动地点
    start     = db.Column(db.String(5), nullable=False)    # 活动开始时间
    end       = db.Column(db.String(5), nullable=False)    # 活动结束时间
    # periods   因为 periods 还依赖于 SPAN， 而 SPAN 可自定义，因此 periods 不应该保存在数据库中
    timestamp = db.Column(db.Integer, nullable=False)      # 最后修改时间
    online    = db.relationship('OnlineOrder', backref='activity', lazy='dynamic')
    onsite    = db.relationship('OnsiteOrder', backref='activity', lazy='dynamic')

    def __init__(self, date, site, start, end, timestamp=None):
        assert regex_activity_date.match(date) is not None
        assert regex_activity_time.match(start) is not None
        assert regex_activity_time.match(end) is not None
        self.date = date
        self.site = site
        self.start = start
        self.end = end
        self.timestamp = int( timestamp or time.time() )

    def __repr__(self):
        return '<%s %d, %s %s-%s, %s>' % (self.__class__.__name__,
                    self.id, self.date, self.start, self.end, self.site)


class OnlineOrder(db.Model):

    __tablename__ = "online_order"

    id          = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    status      = db.Column(db.Integer, nullable=False)   # 订单状态
    user_id     = db.Column(db.String(40), db.ForeignKey('user.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    period      = db.Column(db.Text, nullable=False)      # 预约时段
    model       = db.Column(db.Text, nullable=False)      # 电脑类型
    type        = db.Column(db.Text, nullable=False)      # 问题类型
    desc        = db.Column(db.Text, nullable=False)      # 问题描述
    timestamp   = db.Column(db.Integer, nullable=False)   # 创建时间
    onsite      = db.relationship('OnsiteOrder', backref='online', lazy='dynamic')

    def __init__(self, userID, activityID, period, model, type_, desc="", timestamp=None):
        assert regex_activity_period.match(period) is not None
        assert len(userID) == 40
        self.status = OnlineOrderStatus.VALID
        self.user_id = userID
        self.activity_id = activityID
        self.period = period
        self.model = model
        self.type = type_
        self.desc = desc
        self.timestamp = int( timestamp or time.time() )

    def __repr__(self):
        return '<%s (%d, %d, %d)>' % (self.__class__.__name__,
                    self.id, self.activity_id, self.status)


class OnsiteOrder(db.Model):

    __tablename__ = "onsite_order"

    id          = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    user_id     = db.Column(db.String(40), db.ForeignKey('user.id'), nullable=False)
    online_id   = db.Column(db.Integer, db.ForeignKey('online_order.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    status      = db.Column(db.Integer, nullable=False) # 维修状态
    timestamp   = db.Column(db.Integer, nullable=False) # 创建时间

    def __init__(self, userID, onlineID, activityID, timestamp=None):
        assert len(userID) == 40
        self.user_id = userID
        self.online_id = onlineID
        self.activity_id = activityID
        self.status = OnsiteOrderStatus.WAITING
        self.timestamp = int( timestamp or time.time() )

    def __repr__(self):
        return '<%s (%d, %d, %d, %d>' % (self.__class__.__name__,
                    self.id, self.activity_id, self.online_id, self.status)
