#!/usr/bin/env python3
# -*- coding: utf-8
# filename: tests/test_basic.py

import unittest
from flask import current_app
from app import create_app, db


class TestCaseMixin(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = current_app.test_client()
        self.db = db
        self.db.create_all()

    def tearDown(self):
        #self.db.drop_all()
        self.app_context.pop()

    def check_status_code(self, r, code=200):
        status_code = r.status_code
        self.assertTrue(status_code == code, status_code)

    def check_errcode(self, r):
        respJson = r.get_json()
        errcode = respJson['errcode']
        self.assertTrue(errcode == 0, errcode)


class BasicTestCase(TestCaseMixin):

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])

    def test_db_is_testing(self):
        self.assertTrue(current_app.config["SQLALCHEMY_DATABASE_URI"].endswith("eecs_reboot_test"))

