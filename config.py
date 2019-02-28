#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: config.py

__all__ = [

    "CONFIGS_MAP",

    "DevelopmentConfig",
    "TestingConfig",
    "ProductionConfig",
]


from app.core.secret import MYSQL_USER, MYSQL_PASSWORD, SESSION_KEY


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
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 60 * 5 # 缓存 5 min

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
