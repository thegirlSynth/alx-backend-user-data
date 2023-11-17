#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of the input password
    """

    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_pass
