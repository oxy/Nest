"""
Provides various classes of fun commands.
"""

from .dev import DeveloperFun
from .comics import Comics
from .random import RandomCommands


def setup(bot):
    bot.add_cog(DeveloperFun())
    bot.add_cog(Comics())
    bot.add_cog(RandomCommands())

