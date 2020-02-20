"""
Provides various statistics on bot usage.
"""

from .commands import CommandLogger

def setup(bot):
    if bot.get_cog("PostgreSQL"):
        bot.add_cog(CommandLogger(bot))
