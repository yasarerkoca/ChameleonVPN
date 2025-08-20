"""Application-wide logger configuration."""

import logging
import sys

# Create logger for the application
logger = logging.getLogger("chameleonvpn")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers if this module is imported multiple times
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
