#!/usr/bin/env python3
# -*- coding: utf-8
# filename: config.py

__all__ = [

    "CONFIGS_MAP",

    "DevelopmentConfig",
    "TestingConfig",
    "ProductionConfig",
]


from secret import MYSQL_USER, MYSQL_PASSWORD, SESSION_KEY


def _get_mysql_uri(db):
    return "mysql://{user}:{password}@localhost/{db}".format(
                user=MYSQL_USER, password=MYSQL_PASSWORD, db=db)


class BaseConfigMixin(object):

    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False
    SECRET_KEY = SESSION_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfigMixin):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = _get_mysql_uri("eecs_reboot")
    PORT = 7071


class TestingConfig(BaseConfigMixin):

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = _get_mysql_uri("eecs_reboot_test")


class ProductionConfig(BaseConfigMixin):

    DEBUG = False



CONFIGS_MAP = {

    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,

    }


'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
@staticmethod
def init_app(app):
pass
class DevelopmentConfig(Config):
DEBUG = True
MAIL_SERVER = 'smtp.googlemail.com'
66 | 第 7 章MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
class TestingConfig(Config):
TESTING = True
SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
class ProductionConfig(Config):
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}
'''