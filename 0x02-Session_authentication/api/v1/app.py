#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if os.environ.get("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()

if os.environ.get("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()

if os.environ.get("AUTH_TYPE") == "session_auth":
    from api.v1.auth.session_auth import SessionAuth

    auth = SessionAuth()

if os.environ.get("AUTH_TYPE") == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth

    auth = SessionExpAuth()

if os.environ.get("AUTH_TYPE") == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth

    auth = SessionDBAuth()


@app.before_request
def before_request():
    """
    Filters each request
    """
    if auth:
        path = request.path
        excluded_paths = [
            "/api/v1/status/",
            "/api/v1/unauthorized/",
            "/api/v1/forbidden/",
            "/api/v1/auth_session/login/",
        ]
        check = auth.require_auth(path, excluded_paths)

        if check:
            header = auth.authorization_header(request)
            cookie = auth.session_cookie(request)
            if not header and not cookie:
                abort(401)

            request.current_user = auth.current_user(request)
            user = request.current_user
            if not user:
                abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_request(error) -> str:
    """
    Handler for an unauthorized request
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handler for a forbidden request
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
