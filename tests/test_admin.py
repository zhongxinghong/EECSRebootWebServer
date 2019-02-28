#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: tests/test_admin.py

import unittest
from pprint import pprint
from test_basic import TestCaseMixin


adminid = "rabbit"
password = "210dc3fa530a9e2e92db90b7a23aad3e"


@unittest.skip
class AdminTestCase(TestCaseMixin):

    def test_create(self):
        r = self.client.post("/admin/create", data=self._with_sign(self._with_invitation_auth({
                "adminid": adminid,
                "timestamp": self._get_timestamp(),
            })))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        pprint(respJson)

    @unittest.skip
    def test_forgotten_password(self):
        r = self.client.post("/admin/forgotten_password", data=self._with_sign(self._with_invitation_auth({
                "adminid": adminid,
                "timestamp": self._get_timestamp(),
            })))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        pprint(respJson)