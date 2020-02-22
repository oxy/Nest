"""
Provides core bot functionality and settings management.
"""

from .info import InfoCommands
from .admin import AdminCommands
from .prefix import PrefixManager 
from .locale import LocaleManager
from .error import ErrorHandler

def setup(bot):
    bot.add_cog(InfoCommands())
    bot.add_cog(AdminCommands())
    bot.add_cog(ErrorHandler())

    if bot.get_cog("PrefixStore"):
        bot.add_cog(PrefixManager())
    if bot.get_cog("LocaleStore"):
        bot.add_cog(LocaleManager())
