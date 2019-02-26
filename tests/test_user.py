#!/usr/bin/env python3
# -*- coding: utf-8
# filename: tests/test_user.py

import time
import unittest
from flask import current_app
from app.core.models import User
from app.core.const import MAX_TIMESTAMP_DELAY
from test_basic import TestCaseMixin


openid = "wxid_kdjsalkfjalksjfadsfasfds"


class UserTestCase(TestCaseMixin):

    def test_login(self):
        r = self.client.post("/user/login", data={
                "openid": openid,
                "timestamp": int(time.time() * 1000),
            })
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        userid = respJson['detail']['userid']
        u = User.query.get(userid)
        self.assertFalse(u is None)
        self.assertTrue(u.id == userid)
        self.assertTrue(u.openid == openid)

    @unittest.skip
    def test_login_no_openid(self):
        r = self.client.post("/user/login", data={
                "timestamp": int(time.time() * 1000),
            })
        print(r.get_json())

    @unittest.skip
    def test_login_no_timestamp(self):
        r = self.client.post("/user/login", data={
                "openid": openid,
                "timestamp": int(time.time() * 1000) - MAX_TIMESTAMP_DELAY,
            })
        print(r.get_json())
