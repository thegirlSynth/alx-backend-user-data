#!/usr/bin/env python3
"""
This module contains the SessionDBAuth class
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta

UserSession.load_from_file()


class SessionDBAuth(SessionExpAuth):
    """
    Stores Session IDs in Database
    """

    def create_session(self, user_id=None):
        """
        Create a Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID
        """
        if session_id:
            user_session = UserSession.search({"session_id": session_id})
            if user_session:
                (user_session,) = user_session
                if self.session_duration <= 0:
                    return user_session.user_id

                created_at = user_session.created_at
                if created_at:
                    expiration = created_at + timedelta(
                        seconds=self.session_duration
                    )  # noqa

                    if expiration > datetime.utcnow():
                        return user_session.user_id
        return None

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout
        """
        if request:
            session_id = super().session_cookie(request)
            if session_id:
                session = UserSession.search({"session_id": session_id})
                if session:
                    session[0].remove()
                    return True

        return False
