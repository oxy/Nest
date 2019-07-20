from typing import Dict

import asyncpg
import discord
from discord.ext import commands


class PrefixStore(commands.Cog):
    """
    Provider for prefixes.
    """

    def __init__(self, bot):
        self._db = bot.get_cog("PostgreSQL")

    async def get(self, message: discord.Message):
        """|coro|

        Returns a valid prefix when given a message.

        Parameters
        ----------
        message: discord.Message
            The message to get a prefix for.

        Returns
        -------
        Dict[str, str]
            Dictionary of prefixes per category.
        """
        if message.guild:
            async with self._db.pool.acquire() as conn:
                return await conn.fetchval(
                    "SELECT prefix FROM guild WHERE id=$1",
                    message.guild.id,
                )

    async def set(self, ctx: commands.Context, prefix: str):
        """|coro|

        Sets a valid prefix for .

        Parameters
        ----------
        ctx: commands.Context
            The context to set prefix for.
        data: Dict[str, str]
            Dictionary of prefixes.
        """
        if not ctx.guild:
            return

        async with self._db.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO guild (id, prefix)
                    VALUES ($1, $2)
                    ON CONFLICT (id) DO UPDATE
                        SET (id, prefix) = ($1, $2);
                """,
                ctx.guild.id,
            )
