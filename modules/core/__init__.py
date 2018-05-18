"""
Provides core bot functionality and settings management.
"""

from .user import UserCommands
from .mod import ModCommands

def setup(bot):
    bot.add_cog(UserCommands())
    bot.add_cog(ModCommands())
