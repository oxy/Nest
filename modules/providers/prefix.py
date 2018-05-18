from typing import Dict

from discord.ext import commands
from nest import abc


class PrefixProvider(abc.Provider):
    """
    Provider for prefixes.
    """
    provides = "prefix"

    async def get(self, ctx: commands.Context):
        """|coro|

        Returns a valid prefix when given a message.

        Parameters
        ----------
        bot: client.NestClient
            The bot instance (used for acquiring a database connection).
        message: discord.Message
            The message to get a prefix for.

        Returns
        -------
        Dict[str, str]
            Dictionary of prefixes per category.
        """
        if ctx.message.guild:
            async with ctx.bot.database.acquire() as conn:
                prefixes = await conn.fetchrow(
                    "SELECT user_prefix, mod_prefix FROM prefix WHERE id=$1",
                    ctx.message.guild.id,
                )

            if prefixes:
                prefixes = dict(prefixes)
                return {k.split("_")[0]: v for k, v in prefixes.items()}

        else:
            return {}

    async def set(self, ctx: commands.Context, data: Dict[str, str]):
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

        async with ctx.bot.database.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO prefix (id, user_prefix, mod_prefix)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (id) DO UPDATE
                        SET (id, user_prefix, mod_prefix) = ($1, $2, $3);
                """,
                ctx.guild.id,
                data["user"],
                data["mod"],
                )
