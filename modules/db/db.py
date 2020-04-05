import asyncpg
from discord.ext import commands

class PostgreSQL(commands.Cog):
    def __init__(self, bot):
        self._db = bot.options["database"]
        self.pool = bot.loop.run_until_complete(
            asyncpg.create_pool(database=self._db)
        )
