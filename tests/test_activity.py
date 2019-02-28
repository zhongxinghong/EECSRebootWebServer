#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: tests/test_online.py

import unittest
from app.core.models import Activity
from test_basic import TestCaseMixin
from test_admin import adminid, password


@unittest.skip
class ActivityTestCase(TestCaseMixin):

    def test_create_activity(self):
        r = self.client.post("/activity/create", data=self._with_sign(self._with_admin_auth({
                "adminid": adminid,
                "timestamp": self._get_timestamp(),
                "date": "2018-10-22",
                "site": "二教 410",
                "start": "07:00",
                "end": "09:50",
            }, password)))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        activityid = respJson["detail"]["activityid"]
        self.assertFalse(activityid is None)
        activity = Activity.query.get(activityid)
        self.assertFalse(activity is None)
        print(activityid)
        print(activity)