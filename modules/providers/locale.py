from discord.ext import commands
from nest import abc


class LocaleProvider(abc.Provider):
    provides = "locale"

    async def get(self, ctx: commands.Context):
        """|coro|

        Returns a valid locale when given a context.

        Parameters
        ----------
        ctx: commands.Context
            Context to return a locale for.

        Returns
        -------
        str
            Locale for the given context.
        """
        async with ctx.bot.database.acquire() as conn:
            locale = await conn.fetchval(
                "SELECT locale FROM locale WHERE id=$1", ctx.message.author.id
            )
        return locale

    async def set(self, ctx: commands.Context, data):
        """|coro|

        Sets a valid locale for a given context.

        Parameters
        ----------
        ctx: discord.abc.Messageable
            The context to set prefix for.
        data: Dict[str, str]
            Dictionary of prefixes.
        """
        async with ctx.bot.database.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO locale (id, locale) VALUES ($1, $2) ON CONFLICT (id)
                    DO UPDATE SET (id, locale) = ($1, $2);
                """,
                ctx.author.id,
                data,
            )
