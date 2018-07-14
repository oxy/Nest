"""
Module for utility cogs
"""

from .language import LanguageCommands

def setup(bot):
    bot.add_cog(LanguageCommands())
