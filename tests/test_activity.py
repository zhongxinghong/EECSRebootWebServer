#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: tests/test_online.py

import unittest
from app.core.models import Activity
from test_basic import TestCaseMixin


class ActivityTestCase(TestCaseMixin):

    @unittest.skip
    def test_create_activity(self):
        r = self.client.post("/activity/create", data=self._with_signature({
                "adminid": None,
                "timestamp": self._get_timestamp(),
                "date": "2018-10-22",
                "site": "二教 410",
                "start": "07:00",
                "end": "09:50",
            }))
        self.check_status_code(r)
        self.check_errcode(r)
        respJson = r.get_json()
        activityid = respJson["detail"]["activityid"]
        self.assertFalse(activityid is None)
        activity = Activity.query.get(activityid)
        self.assertFalse(activity is None)
        print(activityid)
        print(activity)