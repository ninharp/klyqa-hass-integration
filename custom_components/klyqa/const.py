"""Constants for the Klyqa Light integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Final

# Integration domain
DOMAIN: Final = "klyqa"

LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=60)

# Attributes
ATTR_ON = "on"
