"""
__init__.py - Initilization for the Database Connection module

Copyright (c) The Hull Seals,
All rights reserved.

Licensed under the GNU General Public License
See license.md
"""

from .connection import (
    NoDatabaseConnection,
    test_database_connection,
)

__all__ = [
    "NoDatabaseConnection",
    "test_database_connection",
]
