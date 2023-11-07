#!/usr/bin/env python3
"""
This module contains the auth class
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manages API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Requires authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Current User
        """
        return None
