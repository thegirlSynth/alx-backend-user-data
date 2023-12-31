#!/usr/bin/env python3
"""
Flask App
"""

from flask import abort, Flask, jsonify, request, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index() -> str:
    """
    GET /
    Return: JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    POST /users
    Return: JSON payload
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    POST /sessions
    Return: Response Object
    """

    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    DELETE /sessions
    """

    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    setattr(user, "session_id", None)

    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
    GET /profile
    Return: JSON payload
    """

    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    email = getattr(user, "email")
    return jsonify({"email": email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST /reset_password
    Return: JSON payload
    """

    try:
        email = request.form.get("email")
        token = AUTH.get_reset_password_token(email)
        return (
            jsonify({"email": email, "reset_token": token}),
            200,
        )

    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    PUT /reset_password
    Return: JSON payload
    """

    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return (
            jsonify({"email": email, "message": "Password updated"}),
            200,
        )

    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
