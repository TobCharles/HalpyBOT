from typing import List
import main
from modules.util.checks import require_permission, DeniedMessage
import logging
from ..util.checks import require_channel

send_to = ["#Repair-Requests", "#Code-Black", "#seal-bob"]

@require_channel()
@require_permission("DRILLED", message=DeniedMessage.DRILLED)
async def manual_case(bot: main, channel: str, sender: str, args: List[str], in_channel: bool):
    message = f"xxxx MANCASE xxxx\n" \
              f"{' '.join(args)}\n" \
              f"xxxx NEWCASE xxxx"
    for ch in send_to:
        await bot.message(ch, message)
        logging.info(f"Manual case by {sender} in {channel}: {args}")
    cn_message = f"New Manual Case Available -- <@&744998165714829334>\n" \
                 f"{' '.join(args)}"
    await bot.message("#case-notify", cn_message)


@require_channel()
@require_permission("DRILLED", message=DeniedMessage.DRILLED)
async def manual_kingfisher(bot: main, channel: str, sender: str, args: List[str], in_channel: bool):
    message = f"xxxx MANKFCASE xxxx\n" \
              f"{' '.join(args)}\n" \
              f"xxxx NEWKFCASE xxxx"
    for ch in send_to:
        await bot.message(ch, message)
        logging.info(f"Manual kingfisher case by {sender} in {channel}: {args}")
    cn_message = f"New Manual KFCase Available -- <@&744998165714829334>\n" \
                 f"{' '.join(args)}"
    await bot.message("#case-notify", cn_message)