#!/usr/bin/env python3
"""
Personal Data
"""
import logging
from typing import List
import re


logging.basicConfig()


def filter_datum(fields: List[str], redaction: str, message: str, separator: str):
    """Returns the log message obfuscated"""
    for field in fields:
        message = re.sub(
            f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message
        )
    return message
