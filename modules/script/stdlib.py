"""
Provide protected functions for the scripter's stdlib.
"""

from discord import Embed
from . import exceptions


async def request(
    ctx, method: str, url: str, params: dict = None, json: bool = False
):
    """|coro|

    Make a request to a webserver.
    All requests and parameters are automatically logged.

    Parameters
    ----------
    method: str
        Method of the request.
    url: str
        URL to send the request to.
    params: dict
        (Optional) Parameter to send.
    json: bool
        (Optional) Decode as json if true.
    """
    async with ctx.bot.database.acquire() as conn:
        await conn.execute(
            """INSERT INTO http (id, meth, url, params, time)
               VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP)""",
            ctx.author.id,
            method,
            url,
            params,
        )

    async with ctx.bot.session.request(method, url, params=params) as resp:
        if not resp.status == 200:
            raise exceptions.HTTPError
        if json:
            ret = await resp.json(content_type=None)
        else:
            ret = await resp.text()
    return ret


async def send(ctx, message: str = None, *, embed: Embed = None):
    if not message and not embed:
        raise ValueError
    ctx.messages.append(await ctx.send(message, embed=embed))
