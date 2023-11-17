#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of the input password
    """

    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_pass


def _generate_uuid() -> str:
    """
    Generates a new uuid
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initializes a DB instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user
        """

        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")

        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_password
            )  # noqa

            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
            return False

        except NoResultFound:
            return False
