#!/usr/bin/env python3
# -*- coding: utf-8
# filename: manage.py

from flask_script import Manager, Server, Shell
from app import create_app, db
from app.core.models import OnlineOrder, OnsiteOrder


app = create_app("default")


def _make_shell_context():
    return {
        "app": app,
        "db": db,
        "OnlineOrder": OnlineOrder,
        "OnsiteOrder": OnsiteOrder,
    }


manager = Manager(app)
manager.add_command("runserver", Server(port=7071))
manager.add_command("shell", Shell(make_context=_make_shell_context))

@manager.command
def test():
    """ Runs the unit tests """
    import unittest
    tests = unittest.TestLoader().discover("tests/")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()