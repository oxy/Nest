"""
Module for utility cogs
"""

from .language import LanguageCommands
from .kitsu import Kitsu
from .dev import PackageLookups
from .gaming import GamingLookups


def setup(bot):
    bot.add_cog(LanguageCommands())
    bot.add_cog(Kitsu())
    bot.add_cog(PackageLookups())
    bot.add_cog(GamingLookups())

