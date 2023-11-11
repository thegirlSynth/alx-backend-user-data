#!/usr/bin/env python3
"""
Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import jsonify, request, session
from models.user import User
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_auth():
    """
    POST /auth_session/login
    Return:
      - The User instance
    """

    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user_list = User.search({"email": email})
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404

    (user,) = user_list

    valid = user.is_valid_password(password)
    if not valid:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    cookie_name = os.environ.get("SESSION_NAME")
    session_user = jsonify(user.to_json())
    session_user.set_cookie(cookie_name, session_id)

    return session_user
