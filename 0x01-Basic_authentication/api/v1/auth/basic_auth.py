#!/usr/bin/env python3
"""
This module contains the BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    This is a class for basic authentication
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:  # noqa
        """
        Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if (
            not authorization_header
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Returns the decoded value of a Base64 string
        """
        if not base64_authorization_header or not isinstance(
            base64_authorization_header, str
        ):
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header).decode(
                "utf-8"
            )  # noqa
            return decoded
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value.
        """
        if (
            not isinstance(decoded_base64_authorization_header, str)
            or ":" not in decoded_base64_authorization_header
        ):
            return (None, None)

        split = decoded_base64_authorization_header.split(":", 1)
        email, password = split

        return (email, password)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """
        Returns the User instance based on his email and password
        """

        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        User.load_from_file()
        user_list = User.search({"email": user_email})
        if not user_list:
            return None

        (user,) = user_list
        valid = user.is_valid_password(user_pwd)
        if not valid:
            return None

        return user

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Overloads Auth and retrieves the User instance for a request.
        """
        header = self.authorization_header(request)
        if header:
            base64_header = self.extract_base64_authorization_header(header)
            if base64_header:
                decoded_header = self.decode_base64_authorization_header(
                    base64_header
                )  # noqa
                if decoded_header:
                    user_credentials = self.extract_user_credentials(
                        decoded_header
                    )  # noqa
                    if user_credentials[0] and user_credentials[1]:
                        user = self.user_object_from_credentials(
                            user_credentials[0], user_credentials[1]
                        )
                        return user
