"""
edsm.py - Elite: Dangerous Star Map API interface module

Copyright (c) The Hull Seals,
All rights reserved.

Licensed under the GNU General Public License
See license.md

Special thanks to TheUnkn0wn1 for his assistance on this module! - https://github.com/theunkn0wn1
"""

from __future__ import annotations
import typing
import math
import asyncio
from pathlib import Path
import json
from time import time
from cattrs.errors import ClassValidationError
from loguru import logger
import aiohttp
import numpy as np
import cattr
from attrs import define, field
from attr import ib
from halpybot import config
from ..exceptions import (
    EDSMConnectionError,
    EDSMReturnError,
    NoResultsEDSM,
    NoNearbyEDSM,
)
from ..models import Coordinates, Location
from ..models import edsm_classes
from ..utils import (
    web_get,
    sys_cleaner,
)


@define(frozen=True)
class EDSMQuery:
    """
    Formulate an EDSM Query and save the time the query was run.
    """

    object: typing.Union[GalaxySystem, Commander, None]
    time: time()


@define(frozen=True)
class EDDBSystem:
    """
    EDDB system object

    System info received from the EDDB formatter packaged in CLI.
    """

    name: str
    dist_star: int
    system_name: str
    coords: Coordinates


@define(frozen=True)
class GalaxySystem:
    """
    EDSM system object

    System info received from the EDSM API.
    """

    name: str
    coords: Coordinates

    _lookupCache = {}

    @classmethod
    def from_api(cls, api: edsm_classes.Galaxy) -> GalaxySystem:
        """
        EDSM Response to System lookup
        """
        return cls(name=api.name, coords=api.coords)

    @classmethod
    async def get_info(
        cls, name, cache_override: bool = False
    ) -> typing.Optional[GalaxySystem]:
        """Get a system object from the EDSM API.

        If the same object was requested less than
        5 minutes ago, it will be retrieved from the internal lookup cache instead. This time
        can be adjusted in config.ini

        Args:
            name (str): The system's name
            cache_override (bool): Disregard caching rules and get directly from EDSM, if true.

        Returns:
            (`GalaxySystem` or None): An EDSM system object, None if unsuccessful.

        Raises:
            EDSMConnectionError: Connection could not be established. Timeout is 10 seconds
                by default.

        """
        name = await sys_cleaner(name)
        # Check if cached
        if name in cls._lookupCache and not cache_override:
            # If less than five minutes ago return stored object
            lookuptime = cls._lookupCache[name].time
            cachetime = config.edsm.time_cached
            if time() < lookuptime + cachetime:
                return cls._lookupCache[name].object

        # Else, get the system from EDSM
        try:
            uri = config.edsm.system_endpoint
            params = {
                "systemName": name,
                "showCoordinates": 1,
                "showInformation": 1,
            }
            responses = await web_get(uri, params)

        except aiohttp.ClientError:
            logger.exception("EDSM: Error in `system get_info()` lookup.")
            raise EDSMConnectionError(
                "Unable to verify system, having issues connecting to the EDSM API."
            ) from aiohttp.ClientError

        # Return None if system doesn't exist
        if len(responses) == 0:
            return None
        try:
            api: edsm_classes.Galaxy = cattr.structure(responses, edsm_classes.Galaxy)
        except ClassValidationError as exc:
            logger.exception("Error validating class. Invalid attributes.")
            raise EDSMReturnError from exc

        # Store in cache and return
        sysobj = GalaxySystem.from_api(api=api)

        cls._lookupCache[name] = EDSMQuery(sysobj, time())
        return sysobj

    @classmethod
    async def exists(cls, name, cache_override: bool = False) -> bool:
        """Check if a system exists in EDSM

        This uses the same caching mechanics as get_info

        Args:
            name (str): The system's name
            cache_override (bool): Disregard caching rules and get directly from EDSM, if true.

        Returns:
            (bool): True if system exists in EDSM, else false

        Raises:
            EDSMConnectionError: Connection could not be established. Timeout is 10 seconds
                by default.

        """
        obj = await cls.get_info(name, cache_override)
        return bool(obj is not None)

    @classmethod
    async def get_nearby(cls, x_coord, y_coord, z_coord):
        """Get a nearby system based on coordinates from the EDSM API.

        Args:
            x_coord (str): The subject x coordinate
            y_coord (str): The subject y coordinate
            z_coord (str): The subject z coordinate

        Returns:
            (tuple): a tuple with the following values:

                - (str or None): An EDSM system object, None if unsuccessful.
                - (str or None): Dist in LY from the coords to the EDSM system object, None if unsuccessful

        Raises:
            EDSMConnectionError: Connection could not be established. Timeout is 10 seconds
                by default.

        """
        # Else, get the system from EDSM
        try:
            uri = config.edsm.sphere_endpoint
            params = {
                "x": x_coord,
                "y": y_coord,
                "z": z_coord,
                "radius": 100,
                "minRadius": 1,
            }
            responses = await web_get(uri, params)
        except aiohttp.ClientError:
            logger.exception("EDSM: Error in `system get_info()` lookup.")
            raise EDSMConnectionError(
                "Unable to verify system, having issues connecting to the EDSM API."
            ) from aiohttp.ClientError

        # Return None if system doesn't exist
        if len(responses) == 0:
            sysname = None
            dist = None
        else:
            sysname = responses[0]["name"]
            dist = responses[0]["distance"]

        return sysname, dist


@define(frozen=True)
class Commander:
    """
    EDSM commander object

    Commander info received from the EDSM API
    """

    # The Four Things We Care About
    msgnum: int
    name: str
    system: str
    coordinates: Coordinates
    date: typing.Optional[str]

    _lookupCache = {}

    @classmethod
    def from_api(cls, name: str, api: edsm_classes.Commander) -> Commander:
        """
        EDSM Response to CMDR Lookup
        """
        return cls(
            msgnum=api.msgnum,
            name=name,
            system=api.system,
            coordinates=api.coordinates,
            date=api.date,
        )

    @classmethod
    async def get_cmdr(
        cls, name, cache_override: bool = False
    ) -> typing.Optional[Commander]:
        """Get info about a CMDR from EDSM

        If the same object was requested less than
        5 minutes ago, it will be retrieved from the internal lookup cache instead. This time
        can be adjusted in config.ini

        Args:
            name (str): CMDR name
            cache_override (bool): Disregard caching rules and get directly from EDSM, if true.

        Returns:
            (`Commander` or None): Commander object if CMDR exists in EDSM, else None

        Raises:
            EDSMConnectionError: Connection could not be established. Timeout is 10 seconds
                by default.

        """

        # Check if cached
        if name.strip().upper() in cls._lookupCache and not cache_override:
            # If less than five minutes ago return stored object
            lookuptime = cls._lookupCache[name.strip().upper()].time
            cachetime = config.edsm.time_cached
            if time() < lookuptime + cachetime:
                return cls._lookupCache[name.strip().upper()].object

        try:
            uri = config.edsm.getpos_endpoint
            params = {"commanderName": name, "showCoordinates": 1}
            responses = await web_get(uri, params)
        except (aiohttp.ClientError, KeyError) as get_cmdr_error:
            logger.exception("EDSM: Error in Commander `get_cmdr()` lookup.")
            raise EDSMConnectionError(
                "Error! Unable to get commander info."
            ) from get_cmdr_error
        # Return None if cmdr doesn't exist
        if len(responses) == 0 or responses["msgnum"] == 203:
            return None
        if responses["msgnum"] == 201:
            raise EDSMConnectionError
        try:
            api: edsm_classes.Commander = cattr.structure(
                responses, edsm_classes.Commander
            )
        except ClassValidationError as exc:
            logger.exception("Error validating class. Invalid attributes.")
            raise EDSMReturnError from exc

        if api.system is None:
            raise EDSMConnectionError("Error! CMDR Exists, but unable to get info.")

        # Store in cache and return
        cmdrobj = Commander.from_api(name=name, api=api)

        cls._lookupCache[name.strip().upper()] = EDSMQuery(cmdrobj, time())
        return cmdrobj

    @classmethod
    async def location(
        cls, name, cache_override: bool = False
    ) -> typing.Optional[Location]:
        """Get a CMDRs location

        Get a Location object for an EDSM commander.

        Args:
            name (str): CMDR name
            cache_override (bool): Disregard caching rules and get directly from EDSM, if true.

        Returns:
            (`Location` or None): CMDRs location if found, else None.

                `Location.system` is the system the cmdr is currently in.
                `Location.coordinates` can be accessed as a dict:

                {
                   "x": Union[float, int],
                   "y": Union[float, int],
                   "z": Union[float, int]
                }

        Raises:
            EDSMConnectionError: Connection could not be established. Timeout is 10 seconds
                by default.

        """
        location = await Commander.get_cmdr(name=name, cache_override=cache_override)
        if location is None:
            return None
        if location.date is None:
            location_time = "an unknown date and time."
        else:
            location_time = location.date
        return Location(
            system=location.system, coordinates=location.coordinates, time=location_time
        )


@define
class Edsm:
    """Carrier, Landmark, and Diversion Systems, formatted for EDSM Usage"""

    _carriers: typing.Optional[typing.List[GalaxySystem]] = ib(default=None)
    _landmarks: typing.Optional[typing.List[GalaxySystem]] = ib(default=None)
    _diversions: typing.Optional[typing.List[EDDBSystem]] = ib(default=None)

    @property
    def landmarks(self):
        """Load pre-defined Landmark systems from file"""
        if self._landmarks:
            return self._landmarks
        landmark_target = Path() / "data" / "edsm" / "landmarks.json"
        if not landmark_target.is_file():
            raise FileNotFoundError
        landmarks = json.loads(landmark_target.read_text())
        self._landmarks = cattr.structure(landmarks, typing.List[GalaxySystem])
        return self._landmarks

    @property
    def carriers(self):
        """Load pre-defined DSSA Carrier systems from file"""
        if self._carriers:
            return self._carriers
        carrier_target = Path() / "data" / "edsm" / "dssa.json"
        if not carrier_target.is_file():
            raise FileNotFoundError
        carriers = json.loads(carrier_target.read_text())
        self._carriers = cattr.structure(carriers, typing.List[GalaxySystem])
        return self._carriers

    @property
    def diversions(self):
        """Load pre-defined diversion systems from file"""
        if self._diversions:
            return self._diversions
        diversions_target = Path() / "data" / "edsm" / "diversions.json"
        if not diversions_target.is_file():
            raise FileNotFoundError
        loaded_diversions = json.loads(diversions_target.read_text())
        self._diversions = cattr.structure(loaded_diversions, typing.List[EDDBSystem])
        return self._diversions


calculators = Edsm()


async def checkdistance(
    sysa: str, sysb: str, cache_override: bool = False
) -> typing.Tuple[str, str]:
    """Check distance between two EDSM points

    Both data points must be known to EDSM.

    Args:
        sysa (str): Either a CMDR or system name
        sysb (str): Either a CMDR or system name
        cache_override (bool): Disregard caching rules and get directly from EDSM, if true.

    Returns:
        (tuple): A tuple with the following values:

            - Distance (str): formatted as xx,yyy.zz
            - Cardinal direction (str): Cardinal direction from point A to B

    Raises:
        EDSMConnectionError: Connection could not be established. Timeout is 10 seconds
                by default.
        NoResultsEDSM: No point was found for either A, B, or both.

    """

    # get both systems at the same time.
    system1, system2 = await asyncio.gather(
        GalaxySystem.get_info(name=sysa, cache_override=cache_override),
        GalaxySystem.get_info(name=sysb, cache_override=cache_override),
    )
    system1: GalaxySystem
    system2: GalaxySystem

    if system1 is None:
        # not a system, maybe a commander?
        cmdr1 = await Commander.location(name=sysa, cache_override=cache_override)
        if cmdr1 is not None:
            system_a = cmdr1.coordinates
        else:
            system_a = None
    else:
        system_a = system1.coords

    if system2 is None:
        cmdr2 = await Commander.location(name=sysb, cache_override=cache_override)
        if cmdr2 is not None:
            system_b = cmdr2.coordinates
        else:
            system_b = None
    else:
        system_b = system2.coords

    # Actually ok that we might be giving cmdr names to sys_cleaner. It won't do anything to names without - in
    if not system_a:
        raise NoResultsEDSM(
            f"No system and/or commander named '{await sys_cleaner(sysa)}' was found in the EDSM "
            f"database."
        )

    if not system_b:
        raise NoResultsEDSM(
            f"No system and/or commander named '{await sys_cleaner(sysb)}' was found in the EDSM "
            f"database."
        )

    distance: float = calc_distance(system_a, system_b)
    formatted_distance: str = f"{distance:,}"
    direction = await calc_direction(system_b.x, system_a.x, system_b.z, system_a.z)
    return formatted_distance, direction


async def checklandmarks(
    edsm_sys_name: str, cache_override: bool = False
) -> typing.Tuple[str, str, str]:
    """Retrieve distance between EDSM point and landmark

    The landmarks used in this function are specified in landmarks.json

    Args:
        edsm_sys_name (str): Name of the EDSM object
        cache_override (bool): Disregard caching rules and get directly from EDSM, if true.

    Returns:

        (tuple): A tuple with the following values:

            - (str): The nearest landmark within the predefined range
            - (str): Distance between point and landmark, in the format xx,yyy.zz
            - (str): The cardinal direction from the landmark to the reference system

    Raises:
        EDSMConnectionError: Connection could not be established. Timeout is 10 seconds
                by default.
        NoResultsEDSM: No point was found for `edsm_sys_name`

    """
    system: str = await sys_cleaner(edsm_sys_name)
    # Set default values
    coords = await get_coordinates(system, cache_override)
    if coords:
        maxdist = config.edsm.maximum_landmark_distance
        distances = {
            calc_distance(coords, item.coords): item for item in calculators.landmarks
        }
        minimum_key = min(distances)
        minimum = distances[minimum_key]

        if minimum_key < float(maxdist):
            direction = await calc_direction(
                coords.x, minimum.coords.x, coords.z, minimum.coords.z
            )
            return minimum.name, f"{minimum_key:,}", direction
        raise NoNearbyEDSM(f"No major landmark systems within 10,000 ly of {system}.")
    raise NoResultsEDSM(
        f"No system and/or commander named {system} was found in the EDSM" f" database."
    )


async def checkdssa(
    edsm_sys_name: str, cache_override: bool = False
) -> typing.Tuple[str, str, str]:
    """Check distance to nearest DSSA carrier

    Last updated 2021-03-22 w/ 93 Carrier

    Args:
        edsm_sys_name (str): System name
        cache_override (bool): Disregard caching rules and get directly from EDSM, if true.

    Returns:
        (tuple): A tuple with the following values:

            - (str): The nearest DSSA Carrier's name
            - (str): Distance between point and DSSA carrier, in the format xx,yyy.zz
            - (str): The cardinal direction to the DSSA Carrier's system

    Raises:
        EDSMConnectionError: Connection could not be established. Timeout is 10 seconds
                by default.
        NoResultsEDSM: No point was found for `edsm_sys_name`.
    """
    system: str = await sys_cleaner(edsm_sys_name)
    coords = await get_coordinates(system, cache_override)
    if coords:
        distances = {
            calc_distance(coords, item.coords): item for item in calculators.carriers
        }

        minimum_key = min(distances)
        minimum = distances[minimum_key]

        direction = await calc_direction(
            coords.x, minimum.coords.x, coords.z, minimum.coords.z
        )
        return minimum.name, f"{minimum_key:,}", direction

    raise NoResultsEDSM(
        f"No system and/or commander named {system} was found in the EDSM" f" database."
    )


@define(frozen=True)
class Diversion:
    """Format for finding Diversion systems"""

    name: str
    system_name: str
    local_direction: str
    dist_star: float = field(converter=float)
    item: float = field(converter=float)


async def diversions(
    edsm_sys_name: str, cache_override: bool = False
) -> typing.List[Diversion]:
    """Check distance to the nearest diversion station

    Last updated 2022-05-23 w/ 7,384 Qualified Stations

    Args:
        edsm_sys_name (str): System name
        cache_override (bool): Disregard caching rules and get directly from EDSM, if true.

    Returns:
        (tuple): Five tuples containing diversion stations and relevant details.

    Raises:
        EDSMConnectionError: Connection could not be established. Timeout is 10 seconds
                by default.
        NoResultsEDSM: No point was found for `edsm_sys_name`.


    """
    coords = await get_coordinates(edsm_sys_name, cache_override)
    if coords:
        distances = {
            calc_distance(coords, item.coords): item for item in calculators.diversions
        }
        local_tup = []
        for value in range(5):
            item = sorted(list(distances.keys()))[value]
            local_min = distances[item]
            local_direction = await calc_direction(
                coords.x, local_min.coords.x, coords.z, local_min.coords.z
            )
            next_nearest = Diversion(
                name=local_min.name,
                dist_star=local_min.dist_star,
                system_name=local_min.system_name,
                local_direction=local_direction,
                item=float(item),
            )
            local_tup.append(next_nearest)
        return local_tup
    raise NoResultsEDSM(
        f"No system and/or commander named {edsm_sys_name} was found in the EDSM"
        f" database."
    )


def calc_distance(loc_a: Coordinates, loc_b: Coordinates) -> float:
    """Calculate distance XYZ -> XYZ

    Only call this method directly when the coordinates of both points are known. If
    only the point names are known, use `edsm/checkdistance` instead.

    Args:
        loc_a (Coordinates): EDSM object coordinates
        loc_b (Coordinates): EDSM object coordinates

    Returns:
        (float): Distance between two points

    """
    point_1 = np.array([loc_a.x, loc_a.y, loc_a.z])
    point_2 = np.array([loc_b.x, loc_b.y, loc_b.z])
    squared_dist = np.sum((point_1 - point_2) ** 2, axis=0)
    dist = np.sqrt(squared_dist)
    dist = np.around(dist, decimals=2)
    return float(dist)


async def calc_direction(
    x_coord_1: typing.Union[int, float],
    x_coord_2: typing.Union[int, float],
    y_coord_1: typing.Union[int, float],
    y_coord_2: typing.Union[int, float],
) -> str:
    """Calculate direction

    Uses some Fancy Math™ to determine the approximate
    cardinal direction in 2D space between two points.

    Args:
        x_coord_1 (int or float): X-coordinate of point A
        x_coord_2 (int or float): X-coordinate of point B
        y_coord_1 (int or float): Y-coordinate of point A
        y_coord_2 (int or float): Y-coordinate of point B

    Returns:
        (str): Cardinal direction from A to B, one of the following values:

            * North
            * NE
            * East
            * SE
            * South
            * SW
            * West
            * NW

    """
    # Treat the coordinates like a right triangle - this is Trig that I swore off of after high school.
    xdeterminer = x_coord_2 - x_coord_1
    ydeterminer = y_coord_2 - y_coord_1
    degrees_temp = math.atan2(xdeterminer, ydeterminer) / math.pi * 180
    # All Coordinates must be Positive.
    if degrees_temp < 0:
        degrees_final = 360 + degrees_temp
    else:
        degrees_final = degrees_temp
    # Round to the nearest degree, treat Directions as an array and compass_lookup as the array item number.
    directions = ["North", "NE", "East", "SE", "South", "SW", "West", "NW", "North"]
    compass_lookup = round(degrees_final / 45)
    result = f"{directions[compass_lookup]}"
    return result


async def get_coordinates(
    edsm_sys_name: str, cache_override: bool = False
) -> typing.Optional[Coordinates]:
    """
    Get the coordinates of a given system in EDSM

    Args:
        edsm_sys_name (str): Name of the system being searched for.
        cache_override (bool): Disregard caching rules and get directly from EDSM, if true.

    Returns:
        ('Coordinates' or None): A coordinate class object if exists, else None.
    """
    sys: typing.Optional[GalaxySystem] = await GalaxySystem.get_info(
        name=edsm_sys_name, cache_override=cache_override
    )
    if sys:
        return sys.coords
    cmdr: typing.Optional[Location] = await Commander.location(
        name=edsm_sys_name, cache_override=cache_override
    )
    return cmdr.coordinates if cmdr else None


async def get_nearby_system(sys_name: str) -> typing.Tuple[bool, typing.Optional[str]]:
    """
    Get a nearby system to a given system in EDSM

    Args:
        sys_name (str): Name of the system being searched for.

    Returns:
        (tuple): A tuple with the following values:
            - (bool): If a system could be located
            - (str or None): The system found, None if False
    """
    name_to_check = await sys_cleaner(sys_name)
    for _ in range(5):
        try:
            uri = config.edsm.systems_endpoint
            params = {"systemName": name_to_check}
            responses = await web_get(uri, params)
            if responses:
                sys = responses[0]["name"]
                return True, sys

            # Cheeky bottom test to not include spaces in the repeat queries and not include it in the 5 request cap
            while True:
                name_to_check = name_to_check[:-1]
                if name_to_check[-1] != " ":
                    break
        except aiohttp.ClientError:
            logger.exception("EDSM: Error in `get_nearby_system()` lookup.")
    return False, None
