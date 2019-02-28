#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: tests/test_root.py

import unittest
from test_basic import TestCaseMixin


@unittest.skip
class RootTestCase(TestCaseMixin):

    def test_get_root(self):
        r = self.client.get("/")
        self.check_status_code(r)
        print(r.data)

    def test_get_timestamp(self):
        r = self.client.get("/get_timestamp")
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        print(respJson['detail']['timestamp'])

    def test_get_robots_txt(self):
        r = self.client.get("/robots.txt")
        self.check_status_code(r, 302)

    def test_get_favicon_ico(self):
        r = self.client.get("/favicon.ico")
        self.check_status_code(r, 302)
