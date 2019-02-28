#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: tests/test_onsite.py

from pprint import pprint
import unittest
from test_basic import TestCaseMixin
from test_user import openid
from test_admin import adminid, password


@unittest.skip
class OnsiteTestCase(TestCaseMixin):

    @unittest.skip
    def test_create_order(self):
        self._login(openid)
        self._get_latest_activity()
        r = self.client.post("/online/get", data=self._with_sign({
                "userid": self.userid,
                "timestamp": self._get_timestamp(),
            }))
        onlineid = r.get_json()['detail']['orderid']
        r = self.client.post("/onsite/create", data=self._with_sign({
                "userid": self.userid,
                "onlineid": onlineid,
                "timestamp": self._get_timestamp(),
            }))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        pprint(respJson)

    @unittest.skip
    def test_current_position(self):
        self._login(openid)
        self._get_latest_activity()
        r = self.client.post("/online/get", data=self._with_sign({
                "userid": self.userid,
                "timestamp": self._get_timestamp(),
            }))
        onlineid = r.get_json()['detail']['orderid']
        r = self.client.post("/onsite/create", data=self._with_sign({
                "userid": self.userid,
                "onlineid": onlineid,
                "timestamp": self._get_timestamp(),
            }))
        onsiteid = r.get_json()["detail"]["onsiteid"]
        r = self.client.post("/onsite/current_position", data=self._with_sign({
                "userid": self.userid,
                "onsiteid": onsiteid,
                "timestamp": self._get_timestamp(),
            }))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        pprint(respJson)


    def test_get_queue(self):
        r = self.client.post("/onsite/queue", data=self._with_sign(self._with_admin_auth({
                "adminid": adminid,
                "timestamp": self._get_timestamp(),
            }, password)))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        pprint(respJson)