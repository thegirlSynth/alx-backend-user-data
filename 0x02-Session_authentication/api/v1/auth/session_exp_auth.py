#!/usr/bin/env python3
"""
This module contains the SessionExpAuth class
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth adds an expiration date to a Session ID
    """

    def __init__(self):
        """
        Initialise a SessionExpAuth instance
        """
        self.session_duration = int(os.environ.get("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """
        Create a Session ID
        """

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {}
        session_dictionary["user_id"] = user_id
        session_dictionary["created_at"] = datetime.now().isoformat()

        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a User ID based on a Session ID
        """
        if session_id:
            session_dictionary = self.user_id_by_session_id.get(session_id)
            if session_dictionary:
                if self.session_duration <= 0:
                    return session_dictionary["user_id"]

                created_at = session_dictionary.get("created_at")
                if created_at:
                    created_at = datetime.fromisoformat(created_at)
                    expiration = created_at + timedelta(
                        seconds=self.session_duration
                    )  # noqa

                    if expiration > datetime.now():
                        return session_dictionary["user_id"]

        return None
