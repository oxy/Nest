"""
Provides core bot functionality and settings management.
"""

from .user import UserCommands
from .mod import ModCommands
from .info import InfoCommands


def setup(bot):
    bot.add_cog(UserCommands())
    bot.add_cog(ModCommands())
    bot.add_cog(InfoCommands())
