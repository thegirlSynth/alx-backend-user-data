#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid
from typing import Optional


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

    def create_session(self, email: str) -> Optional[str]:
        """
        Creates a Session
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            setattr(user, "session_id", session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Find user by session ID
        """
        try:
            if session_id:
                user = self._db.find_user_by(session_id=session_id)
                return user

        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy Session
        """

        try:
            user = self._db.find_user_by(id=user_id)
            setattr(user, "session_id", None)
            return None

        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate reset password token
        """

        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            setattr(user, "reset_token", token)
            return token

        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update Password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            setattr(user, "hashed_password", hashed_password)
            setattr(user, "reset_token", None)

        except NoResultFound:
            raise ValueError
