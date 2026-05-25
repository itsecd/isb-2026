# -*- coding: utf-8 -*-
"""Environment / .env settings parser for HMACTask."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_settings() -> dict:
    """Load and return application settings from environment variables.

    Falls back to sensible defaults when a variable is not set.

    Returns:
        Dictionary with keys:
            - ``secret_key``  – HMAC secret key (str).
            - ``hash_algo``   – Hash algorithm name, e.g. ``"sha256"``.
            - ``messages_file`` – Path to a file with messages to sign.
            - ``output_file``   – Path where signed messages are saved.
    """
    return {
        "secret_key": os.getenv("HMAC_SECRET_KEY", "supersecret"),
        "hash_algo": os.getenv("HMAC_HASH_ALGO", "sha256"),
        "messages_file": os.getenv("MESSAGES_FILE", "messages.txt"),
        "output_file": os.getenv("OUTPUT_FILE", "signed.json"),
    }
