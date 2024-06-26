"""
case.py - The Case Object

Copyright (c) The Hull Seals,
All rights reserved.

Licensed under the GNU General Public License
See license.md
"""

from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from enum import Enum
from attrs import define, field
from pendulum import now, DateTime

if TYPE_CHECKING:
    from halpybot.packages.models import Seal


class Platform(Enum):
    """Storing Platform References"""

    ODYSSEY = 1
    XBOX = 2
    PLAYSTATION = 3
    LEGACY_HORIZONS = 4
    LIVE_HORIZONS = 5
    UNKNOWN = 6


class Status(Enum):
    """Saving Case Status"""

    ACTIVE = 0
    CLOSED = 1
    DELAYED = 2
    INACTIVE = 3


class CaseType(Enum):
    """What Type of Seal Case"""

    SEAL = 1
    BLACK = 2
    BLUE = 3
    FISH = 4


@define(frozen=True)
class KFCoords:
    """KingFisher Coordinate Object"""

    x: float
    y: float


class KFType(Enum):
    """Kingfisher Case Subtypes"""

    LIFT = 0
    GOLF = 1
    PUCK = 2
    PICK = 3


@define(frozen=True, str=False)
class Case:
    """The Case Object - Tracking All The Things!"""

    # All Cases
    # Da Mandatories
    client_name: str
    system: str
    platform: Platform
    board_id: int
    case_type: CaseType
    creation_time: DateTime = field(factory=lambda: now(tz="utc"))
    updated_time: DateTime = field(factory=lambda: now(tz="utc"))
    status: Status = Status.ACTIVE
    welcomed: bool = False
    # Filled As Case Continues
    dispatchers: List[Seal] = field(factory=list)
    responders: List[Seal] = field(factory=list)
    case_notes: list = field(factory=list)
    closed_to: Optional[Seal] = None

    # Da Optionalz
    irc_nick: Optional[str] = None
    can_synth: Optional[bool] = None
    o2_timer: Optional[str] = None

    # For Seal Cases
    hull_percent: Optional[int] = None
    canopy_broken: Optional[bool] = None

    # For Kingfisher Cases
    planet: Optional[str] = None
    pcoords: Optional[KFCoords] = None
    kftype: Optional[KFType] = None

    def __str__(self) -> str:
        """Format case information in a ready-to-be-sent format

        Args:
            self: The Case object in question, from the Case Board

        Returns:
            (str): Fully formatted announcement
        """
        updated = now(tz="utc").diff(self.updated_time).in_words()
        created = now(tz="utc").diff(self.creation_time).in_words()
        plt = self.platform.name.replace("_", " ")
        message = (
            f"Here's the self listing for Case ID {self.board_id}:\n "
            f"General Details: \n"
            f"   Client: {self.client_name}\n"
            f"   System: {self.system}\n"
            f"   Platform: {plt}\n"
            f"   Case Created: {created} ago\n"
            f"   Case Updated: {updated} ago\n"
            f"   Case Status: {self.status.name}\n"
            f"   Client Welcomed: {'Yes' if self.welcomed else 'No'}\n"
        )
        if self.irc_nick:
            message += f"   IRC Nickname: {self.irc_nick}\n"
        if self.closed_to:
            message += f"   Case Closed To: {self.closed_to.name}\n"
        if self.case_type == CaseType.FISH:
            message += (
                f"KF Details:\n"
                f"   Planet: {self.planet}\n"
                f"   Coordinates: {self.pcoords}\n"
                f"   Case Type: {self.kftype.name}\n"
            )
        elif self.case_type in (CaseType.BLACK, CaseType.BLUE):
            message += (
                f"Code Black Details:\n"
                f"   Hull Remaining: {self.hull_percent}\n"
                f"   Canopy Status: {'Broken' if self.canopy_broken else 'Intact'}\n"
                f"   O2 Reported Time: {self.o2_timer}\n"
                f"   Synths Available: {'Yes' if self.can_synth else 'No'}\n"
            )
        else:
            message += f"Case Details:\n" f"   Hull Remaining: {self.hull_percent}\n"
        if self.case_notes:
            case_notes = "\n      ".join(self.case_notes)
        else:
            case_notes = "None Yet!"
        responding_seals = ""
        if self.responders:
            for responder in self.responders:
                responding_seals += f"{responder.name}, "
            responding_seals = responding_seals[:-2]
        responding_spatch = ""
        if self.dispatchers:
            for spatch in self.dispatchers:
                responding_spatch += f"{spatch.name}, "
            responding_spatch = responding_spatch[:-2]
        message += (
            f"Responder Details:\n"
            f"   Dispatchers: {responding_spatch if self.dispatchers else 'None Yet!'}\n"
            f"   Responders: {responding_seals if self.responders else 'None Yet!'}\n"
            f"   Notes: \n      {case_notes}"
        )
        return message
