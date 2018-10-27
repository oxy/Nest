"""
Provides various classes of fun commands.
"""

from .dev import DeveloperFun

def setup(bot):
    bot.add_cog(DeveloperFun)
