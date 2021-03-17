"""
HalpyBOT v1.1

commands\__init__.py - Command initialization script

Copyright (c) 2021 The Hull Seals,
All rights reserved.

Licensed under the GNU General Public License
See license.md
"""

from typing import List
from src.packages.command.commandhandler import Commands

from .announcer import *
from .bot_management import *
from .delayedboard import *
from .fact import *
from .forcejoin import *
from .edsm import *

@Commands.command("ping")
async def cmd_ping(ctx, args: List[str]):
    """
    https://tinyurl.com/yylju9hg
    Ping the bot, to check if it is alive

    Usage: !ping
    Aliases: n/a
    """
    await ctx.reply("Pong!")
