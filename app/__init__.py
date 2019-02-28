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
        return doc.replace("\n", "<br>").replace(" ", "&nbsp;")

    @app.route('/url_maps')
    def get_url_maps():
        return jsonify([repr(r) for r in app.url_map.iter_rules()])

    @app.route('/docs/<endpoint>')
    def get_endpoint_doc(endpoint):
        return _get_doc(endpoint)

    @app.route('/docs')
    @app.route('/docs/')
    def get_docs():
        docs = ""
        for r in app.url_map.iter_rules():
            try:
                doc = _get_doc(r.endpoint)
            except BuildError:
                continue
            else:
                docs += doc
        return docs
