"""
shorten.py - YOURLS URL shortener

Copyright (c) The Hull Seals,
All rights reserved.

Licensed under the GNU General Public License
See license.md
"""

import aiohttp
from loguru import logger
from halpybot import config
from .utils import web_get
from ..exceptions import YOURLSNoResponse, YOURLSBadResponse


async def shorten(url: str) -> str:
    """
    Shorten a given URL via a YOURLS passwordless API call

    Args:
        url (str): The URL to shorten

    Returns:
        surl (str): The shortened URL

    Raises:
        YOURLSNoResponse: YOURLS did not respond by the timeout.
    """
    if not url.lower().startswith("http"):
        url = "https://" + url

    try:
        tgt_uri = f"{config.yourls.uri}/yourls-api.php"
        params = {
            "signature": config.yourls.pwd.get_secret_value(),
            "action": "shorturl",
            "format": "json",
            "url": url,
        }
        responses = await web_get(tgt_uri, params)
    except aiohttp.ClientError as ex:
        logger.exception("YOURLS Did Not Respond")
        raise YOURLSNoResponse from ex

    if not responses:
        raise YOURLSNoResponse
    if "shorturl" not in responses:
        raise YOURLSBadResponse
    return responses["shorturl"]
