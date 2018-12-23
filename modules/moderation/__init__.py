"""
Basic moderation utilities for Birb.
"""

from .staff import CheckMods
from .actions import ModActions

def setup(bot):
    bot.add_cog(CheckMods())
    bot.add_cog(ModActions())

