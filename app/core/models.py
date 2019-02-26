#!/usr/bin/env python3
# -*- coding: utf-8
# filename: models.py

__all__ = [

    "db",

    "User",
    "OnlineOrder",
    "OnsiteOrder",

    ]


import time
from flask_sqlalchemy import SQLAlchemy
from .const import OnsiteOrderStatus, OnlineOrderStatus
from .safety import xSHA1


db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "user"

    id     = db.Column(db.String(40), primary_key=True)
    openid = db.Column(db.Text, nullable=True)
    online = db.relationship('OnlineOrder', backref='user', lazy='dynamic')
    onsite = db.relationship('OnsiteOrder', backref='user', lazy='dynamic')

    def __init__(self, openid):
        self.id = xSHA1(openid)
        self.openid = openid

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.id)


class OnlineOrder(db.Model):

    __tablename__ = "online_order"

    id        = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    user_id   = db.Column(db.String(40), db.ForeignKey('user.id'), nullable=False)
    status    = db.Column(db.Integer, nullable=False)     # 订单状态
    date      = db.Column(db.Date, nullable=False)        # 活动日期
    site      = db.Column(db.Text, nullable=False)        # 活动地点
    period    = db.Column(db.Text, nullable=False)        # 预约时段
    model     = db.Column(db.Text, nullable=False)        # 电脑类型
    type      = db.Column(db.Text, nullable=False)        # 问题类型
    desc      = db.Column(db.Text, nullable=False)        # 问题描述
    timestamp = db.Column(db.Integer, nullable=False)     # 创建时间
    onsite    = db.relationship('OnsiteOrder', backref='online', lazy='dynamic')

    def __init__(self, user_id, date, site, period, model, type, desc="", timestamp=None):
        self.status = OnlineOrderStatus.VALID
        self.user_id = user_id
        self.date = date
        self.site = site
        self.period = period
        self.model = model
        self.type = type
        self.desc = desc
        self.timestamp = int( timestamp or time.time() )

    def __repr__(self):
        return '<%s %d>' % (self.__class__.__name__, self.id)


class OnsiteOrder(db.Model):

    __tablename__ = "onsite_order"

    id        = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    user_id   = db.Column(db.String(40), db.ForeignKey('user.id'), nullable=False)
    online_id = db.Column(db.Integer, db.ForeignKey('online_order.id'), nullable=False)
    status    = db.Column(db.Integer, nullable=False) # 维修状态
    timestamp = db.Column(db.Integer, nullable=False) # 创建时间

    def __init__(self, user_id, online_id, timestamp=None):
        self.user_id = user_id
        self.online_id = online_id
        self.status = OnsiteOrderStatus.Waiting
        self.timestamp = int( timestamp or time.time() )

    def __repr__(self):
        return '<%s (%d, %d)>' % (self.__class__.__name__, self.id, self.online_id)
