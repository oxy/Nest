"""
Module for providers that store data in the database.
"""

from .db import PostgreSQL
from .prefix import PrefixStore
from .locale import LocaleStore


def setup(bot):
    bot.add_cog(PostgreSQL(bot))
    bot.add_cog(PrefixStore(bot))
    bot.add_cog(LocaleStore(bot))
