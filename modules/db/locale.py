from discord.ext import commands


class LocaleStore(commands.Cog):
    def __init__(self, bot):
        self._db = bot.get_cog("PostgreSQL")

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
        async with self._db.pool.acquire() as conn:
            locale = await conn.fetchval(
                "SELECT locale FROM userdata WHERE id=$1",
                ctx.message.author.id,
            )
        return locale

    async def set(self, ctx: commands.Context, locale: str):
        """|coro|

        Sets a valid locale for a given context.

        Parameters
        ----------
        ctx: discord.abc.Messageable
            The context to set prefix for.
        data: Dict[str, str]
            Dictionary of prefixes.
        """
        async with self._db.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO userdata (id, locale) VALUES ($1, $2)
                    ON CONFLICT (id) DO UPDATE SET (id, locale) = ($1, $2);
                """,
                ctx.author.id,
                locale,
            )
