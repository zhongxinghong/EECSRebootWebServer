#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: app/__init__.py

__all__ = [

    "db",

    "create_app",

    ]


from flask import Flask, jsonify, url_for
from config import CONFIGS_MAP
from .core.globals import cache
from .core.models import db
from .blueprints import bpRoot, bpUser, bpActivity, bpOnline, bpOnsite, bpAdmin


def create_app(config_name):

    app = Flask(__name__)
    cfg = CONFIGS_MAP[config_name]
    app.config.from_object(cfg)
    cfg.init_app(app)
    db.init_app(app)
    cache.init_app(app)

    app.register_blueprint(bpRoot)
    app.register_blueprint(bpUser, url_prefix="/user")
    app.register_blueprint(bpActivity, url_prefix="/activity")
    app.register_blueprint(bpOnline, url_prefix="/online")
    app.register_blueprint(bpOnsite, url_prefix="/onsite")
    app.register_blueprint(bpAdmin, url_prefix="/admin")

    _add_rules_help(app)

    return app


def _add_rules_help(app):

    from werkzeug.routing import RequestRedirect, MethodNotAllowed, NotFound, BuildError

    def _get_view_function(url, method='GET'):
        """
        Match a url and return the view and arguments
        it will be called with, or None if there is no view.

        @see  https://stackoverflow.com/questions/38488134/get-the-flask-view-function-that-matches-a-url
        """
        adapter = app.url_map.bind('localhost')

        try:
            match = adapter.match(url, method=method)
        except RequestRedirect as e:
            # recursively match redirects
            return _get_view_function(e.new_url, method)
        except (MethodNotAllowed, NotFound):
            # no match
            return None

        try:
            # return the view function and arguments
            return app.view_functions[match[0]], match[1]
        except KeyError:
            # no view is associated with the endpoint
            return None

    def _esc_doc(doc):
        return doc.replace("\n", "<br>").replace(" ", "&nbsp;")

    def _get_doc(endpoint):
        url = url_for(endpoint)
        res =  _get_view_function(url) or _get_view_function(url, 'POST')
        func, args = res
        doc = ""
        doc += "=== %s ===\n\n" % endpoint
        doc += "path: %s\n" % url
        #doc += "function: %s\n" % func.__name__
        #doc += "arguments: %s\n" % args
        doc += "document: "
        _doc = (func.__doc__ or "").strip()
        if _doc:
            doc += "\n"
            doc += "-" * 40 + "\n"
            doc += _doc + "\n"
            doc += "-" * 40 + "\n"
        else:
            doc += "null\n"
        doc += "\n\n\n"
        return _esc_doc(doc)

    @app.route('/url_maps')
    def get_url_maps():
        return jsonify([repr(r) for r in app.url_map.iter_rules()])

    @app.route('/docs/<endpoint>')
    def get_endpoint_doc(endpoint):
        return _get_doc(endpoint)

    @app.route('/docs')
    @app.route('/docs/')
    def get_docs():
        docs = _esc_doc("""
===================================
EECS-Reboot Development Environment
===================================

通用错误：
    - FormKeyMissingError
    - FormValueTypeError
    - FormValueOutOfRangeError
    - FormValueFormatError
    - InvalidTimestampError


表单字段拼接：
    表单字典按 key 的字典序排序（正常的升序），然后做成 urlencode 形式
    但是不用 escape ，即: raw = "&k1=v1&k2=v2&k3=v3"
    注：表单字段包含 timestamp


鉴权字段构造：
    authorization 字段用来代表某种权限，只有使用正确的 key 构造出的字段，才是有效的

    构造方法：
        首先将表单构造好，通过上述方式获得 raw
        key = "xxxxxx"
        type = "xxxxxx"
        code = hmac(key.encode('utf-8')).md5.hexdigest(raw.encode('utf-8'))
        authorization = "{type} {code}"   # 中间有一个空格

    邀请码鉴权：
        key = 邀请码（64 个字符）
        type = "Invitation"

    管理员鉴权：
        key = 管理员密码（32 个字符）
        type = "Administrator


签名方法：
    signature 字段，是对整个表单的签名，确保表单数据的真实性
    需要在其他字段全部构造完毕的时候再构造这个签名

    构造方法：
        首先将整个表单构造好（包含鉴权字段！），并通过上述方式获得 raw
        signature = md5.hexdigest(raw.encode('utf-8'))

===================================\n\n\n""")
        for r in app.url_map.iter_rules():
            try:
                doc = _get_doc(r.endpoint)
            except BuildError:
                continue
            else:
                docs += doc
        return docs
