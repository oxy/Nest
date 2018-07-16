"""
Module for utility cogs
"""

from .language import LanguageCommands
from .kitsu import Kitsu

def setup(bot):
    bot.add_cog(LanguageCommands())
    bot.add_cog(Kitsu())
