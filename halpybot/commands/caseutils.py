"""
caseutils.py - Commands involving the management of Seal cases

Copyright (c) The Hull Seals,
All rights reserved.

Licensed under the GNU General Public License
See license.md
"""
from typing import List
from pendulum import now
from ..packages.case import format_case_details
from ..packages.command import Commands, get_help_text
from ..packages.models import Context, User, NoUserFound, Case


async def get_case(ctx: Context, case_arg: str) -> Case:
    """Fetch a case from the Board"""
    try:
        caseref = int(case_arg)
    except ValueError:
        caseref = case_arg
    return ctx.bot.board.return_rescue(caseref)


@Commands.command("go")
async def cmd_go(ctx: Context, args: List[str]):
    """
    Check if an assigned Seal is trained and Identified before sending.

    Usage: !go [seals]
    Aliases: n/a
    """
    # If no args presented, skip the user check. This will be removed in later versions, args will be required.
    if args:
        # Clean out the list, only pass "full" args.
        args = [x.strip(" ") for x in args]
        args = [ele for ele in args if ele.strip()]
        # Loop through the list, checking each to see if they are actually a user.
        for seal in args:
            user_level = 1
            # AttributeError is thrown if a user does not exist. Accept and move on.
            try:
                whois = await User.get_info(ctx.bot, str(seal))
                vhost = User.process_vhost(whois.hostname)
            except (AttributeError, NoUserFound):
                vhost = "notUser"
            # There is no hard set "not a seal" vhost level.
            if vhost is None:
                user_level = 0
            if user_level == 0:
                await ctx.reply(
                    f"{ctx.sender}: {str(seal)} is not identified as a trained seal. Have them check their "
                    f"IRC setup?"
                )

    return await ctx.reply(
        await ctx.bot.facts.fact_formatted(fact=("go", "en"), arguments=args)
    )


@Commands.command("listboard")
async def cmd_listboard(ctx: Context, args: List[str]):
    """
    Send a user the key details of every case on the board in DMs

    Usage: !listboard
    Aliases: n/a
    """
    caseboard = ctx.bot.board.by_id
    if not caseboard:
        return await ctx.redirect("The case board is empty!")
    message = "Here's the current case board:\n"
    for case in caseboard.values():
        hskf = "Seal" if case.hull_percent else "Fisher" if case.planet else "Unknown"
        long_ago = now(tz="utc").diff(case.updated_time).in_words()
        plt = case.platform.name.replace("_", " ")
        message += (
            f"Case {case.board_id}: Client: {case.client_name}, Platform: {plt}, "
            f"Type: {hskf}, Status: {case.status.name}, Updated: {long_ago} ago.\n"
        )
    return await ctx.redirect(f"{message}{len(caseboard)} Cases on the Board.")


@Commands.command("listcase")
async def cmd_listcase(ctx: Context, args: List[str]):
    """
    Send a user the key details of a case on the board in DMs

    Usage: !listcase [board ID]
    Aliases: n/a
    """
    if not args:
        return await ctx.reply(get_help_text(ctx.bot.commandsfile, "listcase"))
    try:
        case: Case = await get_case(ctx, args[0])
    except KeyError:
        return await ctx.redirect(f"No case found for {args[0]!r}.")
    return await ctx.redirect(await format_case_details(case))
