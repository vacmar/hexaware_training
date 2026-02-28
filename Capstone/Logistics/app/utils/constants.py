"""
Application constants
"""

# Shipment statuses
SHIPMENT_STATUSES = [
    "created",
    "picked_up",
    "in_transit",
    "at_hub",
    "out_for_delivery",
    "delivered",
    "cancelled",
    "returned"
]

# User roles
USER_ROLES = ["customer", "agent", "admin"]

# Pagination defaults
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# API version
API_VERSION = "v1"

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
