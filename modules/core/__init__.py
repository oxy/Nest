"""
Provides core bot functionality and settings management.
"""

from .info import InfoCommands
from .admin import AdminCommands
from .prefix import PrefixManager 
from .locale import LocaleManager


def setup(bot):
    bot.add_cog(InfoCommands())
    bot.add_cog(AdminCommands())
    if bot.get_cog("PrefixStore"):
        bot.add_cog(PrefixManager())
    if bot.get_cog("LocaleStore"):
        bot.add_cog(LocaleManager())
