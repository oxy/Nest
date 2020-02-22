"""
Provides various classes of fun commands.
"""

from .dev import DeveloperFun
from .comics import Comics
from .images import RandomImages
from .random import RandomCommands
from .reactions import ReactionImages


def setup(bot):
    """Setup cogs."""

    bot.add_cog(DeveloperFun())
    bot.add_cog(Comics())
    bot.add_cog(RandomImages())
    bot.add_cog(RandomCommands())
    bot.add_cog(ReactionImages(bot))
