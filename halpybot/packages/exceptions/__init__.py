"""
__init__.py - Initilization for the Exceptions module

Copyright (c) The Hull Seals,
All rights reserved.

Licensed under the GNU General Public License
See license.md
"""

from .exceptions import (
    YOURLSError,
    YOURLSNoResponse,
    YOURLSBadResponse,
    SpanshError,
    SpanshNoResponse,
    SpanshBadResponse,
    SpanshResponseTimedOut,
    CommandHandlerError,
    CommandException,
    CommandAlreadyExists,
    AnnouncementError,
    KFCoordsError,
    FactUpdateError,
    FactHandlerError,
    InvalidFactException,
    DiscordWebhookError,
    WebhookSendError,
    EDSMLookupError,
    EDSMReturnError,
    EDSMConnectionError,
    NoResultsEDSM,
    NoNearbyEDSM,
    DifferentiateArgsIssue,
    SNSError,
    SubscriptionError,
    NotificationFailure,
    UserError,
    NoUserFound,
    CaseError,
    CaseAlreadyLocked,
    CaseAlreadyExists,
)

__all__ = [
    "YOURLSError",
    "YOURLSNoResponse",
    "YOURLSBadResponse",
    "SpanshError",
    "SpanshNoResponse",
    "SpanshBadResponse",
    "SpanshResponseTimedOut",
    "CommandException",
    "CommandAlreadyExists",
    "CommandHandlerError",
    "AnnouncementError",
    "KFCoordsError",
    "FactHandlerError",
    "FactUpdateError",
    "InvalidFactException",
    "DiscordWebhookError",
    "WebhookSendError",
    "EDSMConnectionError",
    "EDSMReturnError",
    "EDSMLookupError",
    "NoNearbyEDSM",
    "NoResultsEDSM",
    "DifferentiateArgsIssue",
    "SubscriptionError",
    "SNSError",
    "NotificationFailure",
    "UserError",
    "NoUserFound",
    "CaseError",
    "CaseAlreadyLocked",
    "CaseAlreadyExists",
]
