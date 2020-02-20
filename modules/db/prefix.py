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
        str
            Prefix set by guild, if any.
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
        prefix: str
            Prefix to set.
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
                (ctx.guild.id, prefix),
            )
