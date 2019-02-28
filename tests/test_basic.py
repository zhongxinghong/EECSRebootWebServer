#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: tests/test_basic.py

import time
from pprint import pprint
import unittest
from flask import current_app
from app import create_app, db
from app.core.safety import get_signature
from app.blueprints.activity import _get_latest_activity


class TestCaseMixin(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = current_app.test_client()
        self.db = db
        self.db.create_all()

    def tearDown(self):
        #self.db.drop_all()
        self.db.session.remove()
        self.ctx.pop()

    def check_status_code(self, r, code=200):
        status_code = r.status_code
        try:
            self.assertTrue(status_code == code, status_code)
        except AssertionError as e:
            pprint(r.get_json())
            raise e

    def check_errcode(self, r):
        respJson = r.get_json()
        errcode = respJson['errcode']
        try:
            self.assertTrue(errcode == 0, errcode)
        except AssertionError as e:
            pprint(r.get_json())
            raise e

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _login(self, openid):
        if hasattr(self, "userid"):
            return
        r = self.client.post("/user/login", data=self._with_signature({
                "openid": openid,
                "timestamp": self._get_timestamp(),
            }))
        respJson = r.get_json()
        self.userid = respJson["detail"]["userid"]

    def _get_latest_activity(self):
        if not hasattr(self, "activity") or not hasattr(self, "periods"):
            activity, periods = _get_latest_activity()
            self.activity = activity
            self.periods = periods

    def _with_signature(self, data):
        signature = get_signature(data)
        return dict(
                signature = signature,
                **data,
            )


class BasicTestCase(TestCaseMixin):

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])

    def test_db_is_testing(self):
        self.assertTrue(current_app.config["SQLALCHEMY_DATABASE_URI"].endswith("eecs_reboot_test"))

