"""
Module for utility cogs
"""

from .language import LanguageCommands
from .kitsu import Kitsu
from .dev import PackageLookups


def setup(bot):
    bot.add_cog(LanguageCommands())
    bot.add_cog(Kitsu())
    bot.add_cog(PackageLookups())
