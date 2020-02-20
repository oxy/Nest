"""
Log usage of commands.
"""

from discord.ext import commands


class CommandLogger(commands.Cog):
    def __init__(self, bot):
        self._db = bot.get_cog("PostgreSQL")

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        """|coro|

        Logs a command.

        Parameters
        ----------
        ctx: commands.Context
            The context to log.
        """
        async with self._db.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO command (id, command, message, user, guild) VALUES ($1, $2, $3, $4, $5)
                """,
                ctx.message.id,
                ctx.command.name,
                ctx.message.content,
                ctx.author.id,
                ctx.guild.id if ctx.guild else None
            )
