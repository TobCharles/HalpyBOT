"""
HalpyBOT v1.6

shutdown.py - Will be with you shortly, please hold!

Copyright (c) 2022 The Hull Seals,
All rights reserved.

Licensed under the GNU General Public License
See license.md
"""


import os
import signal
from typing import List
from loguru import logger
from ..packages.checks import Require, Admin
from ..packages.command import Commands
from ..packages.models import Context


@Commands.command("shutdown", "restart", "sealpukku", "reboot")
@Require.direct_message()
@Require.permission(Admin)
async def cmd_shutdown(ctx: Context, args: List[str]):
    """
    Shut down the bot (restart if running as daemon)

    Usage: !shutdown
    Aliases: !reboot
    """
    logger.critical("Shutdown has been ordered by {sender}", sender=ctx.sender)
    await ctx.bot.quit(f"HalpyBOT restart ordered by {ctx.sender}. Stand By.")
    os.kill(os.getpid(), signal.SIGTERM)
