# -*- coding: utf-8 -*-
"""Logging configuration for HMACTask."""

import logging
import sys


def setup_logger(name: str = "HMACTask", level: str = "INFO") -> logging.Logger:
    """Set up and return a named logger with a console handler.

    Args:
        name: Logger name displayed in log records.
        level: Logging level string (DEBUG, INFO, WARNING, ERROR).

    Returns:
        Configured :class:`logging.Logger` instance.
    """
    log = logging.getLogger(name)
    log.setLevel(getattr(logging, level.upper(), logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    if not log.handlers:
        log.addHandler(handler)

    return log


app_logger = setup_logger()
