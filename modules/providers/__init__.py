"""
Module for providers that store data in the database.
"""

from .prefix import PrefixProvider
from .locale import LocaleProvider 

def setup(bot):
    if bot.has_features("database"):
        bot.add_provider(PrefixProvider())
        bot.add_provider(LocaleProvider())
