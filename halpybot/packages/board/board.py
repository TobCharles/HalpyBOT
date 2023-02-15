"""
board.py - Internal Case Board

Copyright (c) The Hull Seals,
All rights reserved.

Licensed under the GNU General Public License
See license.md
"""
from __future__ import annotations
import typing
from asyncio import Lock
from pendulum import now


class TempRescue:
    """TODO: Replace with Real Rescue Type"""

    pass


class Board:
    """
    Internal Case Board - Tracking Cases Cleanly
    """

    def __init__(self, id_range):
        """Initalize the Board"""
        self._cases_by_id: typing.Dict[int, TempRescue] = {}
        self._cases_by_name: typing.Dict[str, TempRescue] = {}
        self._case_index = None
        self._last_case_time = None
        self._modlock = Lock()
        self._id_range: int = id_range

    @property
    def next_case_id(self) -> int:
        """Returns the next valid Case ID"""
        return 4

    @property
    def time_last_case(self):
        """Time since the last case started"""
        return self._last_case_time

    def _update_last_index(self):
        """Update the last case time index"""
        self._last_case_time = now(tz="utc")

    def __getitem__(self, key: typing.Union[str, int]) -> TempRescue | None:
        if isinstance(key, str):
            return self._cases_by_name[key.casefold()]
        if isinstance(key, int):
            return self._cases_by_id[key]
        return None

    async def new_rescue(self):
        pass

    async def mod_rescue(self):
        pass

    async def del_rescue(self):
        pass

    """
    TODO
    1) Create Local Case IDs
    2) Create a Case
    3) Update a Case
    4) Delete a Case
    """
