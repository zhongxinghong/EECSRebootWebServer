#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: tests/test_online.py

import random
from pprint import pprint
import unittest
from app.core.const import REPAIR_TYPES
from app.core.models import OnlineOrder
from test_basic import TestCaseMixin
from test_user import openid


class OnlineTestCase(TestCaseMixin):

    @unittest.skip
    def test_create_order(self):
        self._login(openid)
        self._get_latest_activity()
        r = self.client.post("/online/create", data=self._with_signature({
                "userid": self.userid,
                "model": "ThinkPad X230",
                "type": random.choice(REPAIR_TYPES),
                "desc": "测试啦哈哈哈%s" % self._get_timestamp(),
                "period": random.choice(self.periods),
                "timestamp": self._get_timestamp(),
            }))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        orderid = respJson["detail"]["orderid"]
        self.assertFalse(orderid is None)
        order = OnlineOrder.query.get(orderid)
        self.assertFalse(order is None)
        print(orderid)
        print(order)

    #@unittest.skip
    def test_get_order(self):
        self._login(openid)
        self._get_latest_activity()
        r = self.client.post("/online/get", data=self._with_signature({
                "userid": self.userid,
                "timestamp": self._get_timestamp(),
            }))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        pprint(respJson)

    @unittest.skip
    def test_withdraw_order(self):
        self._login(openid)
        self._get_latest_activity()
        r = self.client.post("/online/get", data=self._with_signature({
                "userid": self.userid,
                "timestamp": self._get_timestamp(),
            }))
        orderid = r.get_json()["detail"]["orderid"]
        pprint(r.get_json())
        r = self.client.post("/online/withdraw", data=self._with_signature({
                "userid": self.userid,
                "orderid": orderid,
                "timestamp": self._get_timestamp(),
            }))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        pprint(respJson)


    @unittest.skip
    def test_get_order_signature(self):
        self._login(openid)
        self._get_latest_activity()
        r = self.client.post("/test_signature", data=self._with_signature({
                "userid": self.userid,
                "timestamp": self._get_timestamp(),
            }))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        pprint(respJson)


    def test_get_all(self):
        r = self.client.post("/online/all", data=self._with_signature({
                "adminid": "dajflkajdslfjkdsaf",
                "timestamp": self._get_timestamp(),
            }))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        pprint(respJson)