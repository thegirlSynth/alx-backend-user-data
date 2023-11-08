#!/usr/bin/env python3
"""
This module contains the BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64


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
            not decoded_base64_authorization_header
            or not isinstance(decoded_base64_authorization_header, str)
            or ":" not in decoded_base64_authorization_header
        ):
            return (None, None)

        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header.split(":")[1]

        return (email, password)
