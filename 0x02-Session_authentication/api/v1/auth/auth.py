#!/usr/bin/env python3
"""
This module contains the Auth class
"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Manages API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Requires authentication
        """

        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True

        if not path.endswith("/"):
            path += "/"

        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        Authorization header
        """
        if request is None or "Authorization" not in request.headers:
            return None

        authorization_header = request.headers.get("Authorization")
        return authorization_header

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Current User
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        """

        if not request:
            return None

        session_id = os.environ.get("SESSION_NAME")
        cookie = request.cookies.get(session_id)

        return cookie
