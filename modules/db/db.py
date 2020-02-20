import asyncpg
from discord.ext import commands

class PostgreSQL(commands.Cog):
    def __init__(self, bot):
        self._db = bot.options["database"]
        self.pool: asyncpg.pool.Pool = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.pool = await asyncpg.create_pool(database=self._db)
