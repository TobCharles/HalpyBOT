"""
test_commands.py - What are your orders, Captain?

Copyright (c) The Hull Seals,
All rights reserved.

Licensed under the GNU General Public License
See license.md
"""

import pytest
from halpybot.packages.command import Commands
from halpybot import config

# noinspection PyUnresolvedReferences
from .fixtures.mock_edsm import mock_api_server_fx

# noinspection PyUnresolvedReferences
from .fixtures.mock_board import mock_full_board_fx

config.offline_mode.enabled = False
config.edsm.uri = "http://127.0.0.1:4000"


@pytest.mark.asyncio
async def test_ping(bot_fx):
    """Check the ping command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}ping",
    )
    assert bot_fx.sent_messages[0] == {"message": "Pong!", "target": "#bot-test"}


@pytest.mark.asyncio
async def test_serverping(bot_fx):
    """Check the serverstatus command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}serverstatus",
    )
    assert bot_fx.sent_messages[0].get("message").startswith("The Elite servers are")


@pytest.mark.asyncio
async def test_botping_dm(bot_fx):
    """Check the PING command in DMs"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="generic_seal",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}ping",
    )
    assert bot_fx.sent_messages[0] == {"message": "Pong!", "target": "generic_seal"}


@pytest.mark.asyncio
async def test_lookup(bot_fx):
    """Test the lookup command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}lookup Sol",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "System SOL exists in EDSM",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_lookup_2(bot_fx):
    """Test the lookup command with no arguments"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}lookup",
    )
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"
    assert bot_fx.sent_messages[0].get("message").startswith("Use: ")
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .endswith("Check if a system exists in EDSM")
    )


@pytest.mark.asyncio
async def test_lookup_3(bot_fx):
    """Test the lookup command with an invalid system"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}lookup PRAISEHALPYDAMNWHYISTHISNOTASYSNAM",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "System PRAISEHALPYDAMNWHYISTHISNOTASYSNAM not found in EDSM",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_lookup_4(bot_fx):
    """Test the Lookup command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}lookup --new Sol",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "System SOL exists in EDSM",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_drillcase(bot_fx):
    """Test the drillcase command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}drillcase Rixxan, PC, Delkar, 90",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "xxxx DRILL -- DRILL -- DRILL xxxx\n"
        "CMDR: Rixxan -- Platform: PC\nSystem: DELKAR -- Hull: 90\nxxxxxxxx",
        "target": "#bot-test",
    }
    assert bot_fx.sent_messages[1] == {
        "message": "System exists in EDSM, 83.11 LY NE of Sol.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_drillcase_unauth(bot_fx):
    """Test the drillcase command with an unauthorized user"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_pup",
        message=f"{config.irc.command_prefix}drillcase Rixxan, PC, Delkar, 90",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "You have to be a drilled seal to use this!",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_drillcase_unauth_guest(bot_fx):
    """Test the drillcase command as a guest"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="guest_user",
        message=f"{config.irc.command_prefix}drillcase Rixxan, PC, Delkar, 90",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "You have to be a drilled seal to use this!",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_help(bot_fx):
    """Test the help command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="guest_user",
        message=f"{config.irc.command_prefix}help",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "Responding in DMs!",
        "target": "#bot-test",
    }
    assert bot_fx.sent_messages[1].get("target") == "guest_user"
    assert bot_fx.sent_messages[1].get("message") is not False


@pytest.mark.asyncio
async def test_help_specific(bot_fx):
    """Test the help command on a specific argument"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="guest_user",
        message=f"{config.irc.command_prefix}help ping",
    )
    assert bot_fx.sent_messages[0] == {
        "message": f"Use: {config.irc.command_prefix}ping  \nCheck to see if the bot is responding to commands.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_help_multiple(bot_fx):
    """Test the HELP command with multiple commands"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="guest_user",
        message=f"{config.irc.command_prefix}help ping dssa",
    )
    assert bot_fx.sent_messages[0] == {
        "message": f"Use: {config.irc.command_prefix}ping  \nCheck to see if the bot is responding to commands.",
        "target": "#bot-test",
    }
    assert bot_fx.sent_messages[1] == {
        "message": f"Use: {config.irc.command_prefix}dssa [EDSM Valid Location] \nCheck for the closest DSSA carrier to a given location.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_help_none(bot_fx):
    """Test the help command without arguments"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="guest_user",
        message=f"{config.irc.command_prefix}help spaghetti",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "The command spaghetti could not be found in the list. Try running help without an argument to get the list of commands",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_about(bot_fx):
    """Test the ABOUT command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="guest_user",
        message=f"{config.irc.command_prefix}about",
    )
    assert bot_fx.sent_messages[1].get("target") == "guest_user"
    assert (
        bot_fx.sent_messages[1]
        .get("message")
        .endswith("in the development of HalpyBOT.")
    )


@pytest.mark.asyncio
async def test_say_channel(bot_fx):
    """Test the SAY command in a channel"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_user",
        message=f"{config.irc.command_prefix}say #bot-test bacon and eggs",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "Responding in DMs!",
        "target": "#bot-test",
    }
    assert bot_fx.sent_messages[1] == {
        "message": "You have to run that command in DMs with me!",
        "target": "some_user",
    }


@pytest.mark.asyncio
async def test_utc(bot_fx):
    """Test the UTC command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_user",
        message=f"{config.irc.command_prefix}utc",
    )
    assert bot_fx.sent_messages[0].get("message").startswith("It is currently")
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"


@pytest.mark.asyncio
async def test_year(bot_fx):
    """Test the YEAR command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_user",
        message=f"{config.irc.command_prefix}year",
    )
    assert bot_fx.sent_messages[0].get("message").startswith("It is currently the year")
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"


@pytest.mark.asyncio
async def test_say_direct_unauth(bot_fx):
    """Test the SAY command with an unauthorized user"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="some_admin",
        sender="some_admin",
        message=f"{config.irc.command_prefix}say #bot-test bacon and eggs",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "No.",
        "target": "some_admin",
    }


@pytest.mark.asyncio
async def test_say(bot_fx):
    """Test the SAY command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="some_cyber",
        sender="some_cyber",
        message=f"{config.irc.command_prefix}say #bot-test bacon and eggs",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "bacon and eggs",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_say_no_args(bot_fx):
    """Test the say command without arguments"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="some_cyber",
        sender="some_cyber",
        message=f"{config.irc.command_prefix}say",
    )
    assert bot_fx.sent_messages[0] == {
        "message": f"Use: {config.irc.command_prefix}say [channel] [text] \nMake the Bot say something",
        "target": "some_cyber",
    }


@pytest.mark.asyncio
async def test_whois_hbot(bot_fx):
    """Test the WHOIS command easter egg"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="some_admin",
        sender="some_admin",
        message=f"{config.irc.command_prefix}whois halpybot",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "That's me! CMDR HalpyBOT has a Seal ID of 0, registered 14.8 billion years ago, is a DW2 Veteran and Founder Seal with registered CMDRs of Arf! Arf! Arf!, and has been involved with countless rescues.",
        "target": "some_admin",
    }


@pytest.mark.asyncio
async def test_whois_empty(bot_fx):
    """Test the WHOIS command without arguments"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="some_admin",
        sender="some_admin",
        message=f"{config.irc.command_prefix}whois",
    )
    assert bot_fx.sent_messages[0] == {
        "message": f"Use: {config.irc.command_prefix}whois [name] \nCheck the user information for registered name. Must be a registered user, and run in DMs with HalpyBOT.",
        "target": "some_admin",
    }


# FIXME: These two tests need to be reworked to avoid poking the live DB.
@pytest.mark.asyncio
async def test_whois(bot_fx):
    """Test the WHOIS command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="some_admin",
        sender="some_admin",
        message=f"{config.irc.command_prefix}whois Rixxan",
    )
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .startswith("CMDR Rixxan has a Seal ID of 1")
    )


@pytest.mark.asyncio
async def test_whoami(bot_fx):
    """Test the WHOAMI command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="Rixxan",
        sender="Rixxan",
        message=f"{config.irc.command_prefix}whoami",
    )
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .startswith("CMDR Rixxan has a Seal ID of 1")
    )


@pytest.mark.asyncio
async def test_edsmping(bot_fx):
    """Test the EDSM Ping command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_cyber",
        message=f"{config.irc.command_prefix}edsmping",
    )
    assert bot_fx.sent_messages[0].get("message").startswith("EDSM Latency: ")
    assert bot_fx.sent_messages[0].get("message").endswith("seconds")
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"


@pytest.mark.asyncio
async def test_drill_empty(bot_fx):
    """Test the drill command without arguments"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}drillcase",
    )
    assert bot_fx.sent_messages[0] == {
        "message": f"Use: {config.irc.command_prefix}drillcase [cmdr], [platform], [system], [hull] \nStarts a new Drill Case, separated by Commas",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_drillkf_empty(bot_fx):
    """Test what happens if the KF Drill case can be run without arguments"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}drillkfcase",
    )
    assert bot_fx.sent_messages[0] == {
        "message": f"Use: {config.irc.command_prefix}drillkfcase [cmdr], [platform], [system], [planet], [coords], [type] \nStarts a new Drill Kingfisher Case, separated by Commas",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_drillcb_empty(bot_fx):
    """Test if the CB drill case can be run without arguments"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}drillcbcase",
    )
    assert bot_fx.sent_messages[0] == {
        "message": f"Use: {config.irc.command_prefix}drillcbcase [cmdr], [platform], [system], [hull], [cansynth], [o2] \nStarts a new Drill CB Case, separated by Commas",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_drillkf(bot_fx):
    """Test the KF drill command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}drillkfcase Rixxan, PC, Delkar, 3 a, 123.456, 123.456, Puck",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "xxxx DRILL -- DRILL -- DRILL xxxx\n"
        "CMDR: Rixxan -- Platform: PC\n"
        "System: DELKAR -- Planet: 3 a\n"
        "Coordinates: 123.456\n"
        ":Type: 123.456\n"
        "xxxxxxxx",
        "target": "#bot-test",
    }
    assert bot_fx.sent_messages[1] == {
        "message": "System exists in EDSM, 83.11 LY NE of Sol.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_drillkf_unauth(bot_fx):
    """Test if the KF drill case can be fired by an unauthorized user"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_pup",
        message=f"{config.irc.command_prefix}drillkfcase Rixxan, PC, Delkar, 3 a, 123.456, 123.456, Puck",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "You have to be a drilled seal to use this!",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_drillcb(bot_fx):
    """Test if the code black drill command can be run"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}drillcbcase Rixxan, PC, Delkar, 25, No, 12:34",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "xxxx DRILL -- DRILL -- DRILL xxxx\nCMDR: Rixxan -- Platform: PC\nSystem: DELKAR -- Hull: 25\nCan Synth: No -- O2 Timer: 12:34\nxxxxxxxx",
        "target": "#bot-test",
    }
    assert bot_fx.sent_messages[1] == {
        "message": "System exists in EDSM, 83.11 LY NE of Sol.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_drillcb_unauth(bot_fx):
    """Test if the drillCB command can be fired by an unauthorized user"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_pup",
        message=f"{config.irc.command_prefix}drillcbcase",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "You have to be a drilled seal to use this!",
        "target": "#bot-test",
    }


# TODO: Stop Touching Database
@pytest.mark.asyncio
async def test_go_valid(bot_fx):
    """Test the GO command"""
    await mock_full_board_fx(bot_fx)
    await bot_fx.facts._from_local()
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}go 1 Rixxan",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "Rixxan: You're up.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_go_guest(bot_fx):
    """Test the GO command"""
    await mock_full_board_fx(bot_fx)
    await bot_fx.facts._from_local()
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}go 1 guest_user",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "generic_seal: guest_user is not identified as a trained seal. Have them check their IRC setup?",
        "target": "#bot-test",
    }
    assert bot_fx.sent_messages[1] == {
        "message": "guest_user: You're up.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_locate(bot_fx):
    """Test the locate command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}locate Rixxan",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "CMDR Rixxan was last seen in Pleiades Sector HR-W d1-79 on 2022-03-15 20:51:01",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_locate_malformed_response(bot_fx):
    """Test the locate command when EDSM gives a malformed or incomplete response"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}locate Abildgaard Jadrake",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "Received a reply from EDSM about Abildgaard Jadrake, but could not process the return.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_locate_2(bot_fx):
    """Test the locate command with no arguments"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}locate",
    )
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"
    assert bot_fx.sent_messages[0].get("message").startswith("Use: ")
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .endswith("Check if a CMDR exists and shares their location in EDSM")
    )


@pytest.mark.asyncio
async def test_locate_3(bot_fx):
    """Test the locate command with an invalid name"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}locate Praisehalpydamnwhyisthisnotacmdrnam",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "CMDR not found or not sharing location on EDSM",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_locate_4(bot_fx):
    """Test the locate command cache override"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}locate --new Rixxan",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "CMDR Rixxan was last seen in Pleiades Sector HR-W d1-79 on 2022-03-15 20:51:01",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_distance(bot_fx):
    """Test the distance command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}distance Rixxan : Delkar",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "RIXXAN is 444.35 LY South of DELKAR.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_distance_2(bot_fx):
    """Test the distance command with no arguments"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}distance",
    )
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"
    assert bot_fx.sent_messages[0].get("message").startswith("Use: ")
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .endswith("Check the distance between two points in EDSM")
    )


@pytest.mark.asyncio
async def test_distance_3(bot_fx):
    """Test the distance command with an invalid value"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}dist Rixxan: Praisehalpydamnwhyisthisnotacmdrnam",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "Failed to query EDSM for system or CMDR details.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_distance_4(bot_fx):
    """Test the distance command with cache override"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}dist --new Rixxan: Delkar",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "RIXXAN is 444.35 LY South of DELKAR.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_coords(bot_fx):
    """Test the coords command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}coords 1 2 3",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "Hixkar is 98.25 LY from 1, 2, 3.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_coords_2(bot_fx):
    """Test the coords command with no arguments"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}coords",
    )
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"
    assert bot_fx.sent_messages[0].get("message").startswith("Use: ")
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .endswith("Check EDSM for a nearby system to a set of coordinates")
    )


@pytest.mark.asyncio
async def test_coords_3(bot_fx):
    """Test the coords command with an invalid value"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}coords 1 2 h",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "All coordinates must be numeric.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_coords_4(bot_fx):
    """Test the coords command with an invalid EDSM value"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="generic_seal",
        message=f"{config.irc.command_prefix}coords 1000000000 20000000000 30000000000",
    )
    assert bot_fx.sent_messages[0] == {
        "message": "No systems known to EDSM within 100ly of 1000000000, 20000000000, 30000000000.",
        "target": "#bot-test",
    }


@pytest.mark.asyncio
async def test_diversion(bot_fx):
    """Test the diversion command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_user",
        message=f"{config.irc.command_prefix}diversion Sol",
    )
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .startswith("Closest Diversion Stations to SOL:")
    )
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"


@pytest.mark.asyncio
async def test_dssa(bot_fx):
    """Test the DSSA command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_user",
        message=f"{config.irc.command_prefix}dssa Sol",
    )
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .startswith("The closest DSSA Carrier is in")
    )
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"


@pytest.mark.asyncio
async def test_landmark(bot_fx):
    """Test the landmark command"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_user",
        message=f"{config.irc.command_prefix}landmark Sol",
    )
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .startswith("The closest landmark system is")
    )
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"


@pytest.mark.asyncio
async def test_fireball(bot_fx):
    """Test the Fireball and Dice Rolling Commands"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_pup",
        message=f"{config.irc.command_prefix}fireball",
    )
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .startswith("Kawoosh! some_pup cast a fireball on chat! Rolling for damage...")
    )
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"
    assert bot_fx.sent_messages[1].get("message").startswith("some_pup:")


@pytest.mark.asyncio
async def test_roll_bad(bot_fx):
    """Test the Fireball and Dice Rolling Commands"""
    await Commands.invoke_from_message(
        bot=bot_fx,
        channel="#bot-test",
        sender="some_pup",
        message=f"{config.irc.command_prefix}roll bacon",
    )
    assert (
        bot_fx.sent_messages[0]
        .get("message")
        .startswith("Use: ^roll #d# \nRoll the dice! (Up to 10 dice of any size)")
    )
    assert bot_fx.sent_messages[0].get("target") == "#bot-test"
