"""
Provides core features, such as ping.
"""
import time
from discord.ext import commands


class CoreCommands:
    category = "user"

    @commands.command()
    async def ping(self, ctx):
        pre_typing = time.monotonic()
        await ctx.trigger_typing()
        latency = int(round((time.monotonic() - pre_typing) * 1000))
        await ctx.send(ctx._("ping_response").format(latency))


def setup(bot):
    bot.add_cog(CoreCommands())
