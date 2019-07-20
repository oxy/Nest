"""
NSFW image search commands to grab images from various boorus.
"""

from .images import NSFW

def setup(bot):
    bot.add_cog(NSFW(bot))
