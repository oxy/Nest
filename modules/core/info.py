"""
Provides informational commands.

:copyright: (c) 2017 Jakeoid, 2018 n303p4, 2019 Oxylibrium.
:license: MIT, see LICENSE.md for details.
"""

import time
import sys
from datetime import datetime

import discord
from discord.ext import commands
from dateutil.relativedelta import relativedelta


class InfoCommands(commands.Cog):
    @commands.command(aliases=["info"])
    async def stats(self, ctx):
        """Display statistics about the bot."""
        uptime = relativedelta(datetime.now(), ctx.bot.created)

        text = ctx._("information").format(
            bot=ctx.bot.user.name,
            guilds=len(ctx.bot.guilds),
            channels=sum(1 for _ in ctx.bot.get_all_channels()),
            users=sum(1 for _ in ctx.bot.get_all_members()),
            uptime=ctx.bot.i18n.format_timedelta(ctx.locale, uptime),
            commands=len(ctx.bot.commands),
        )

        await ctx.send(text)

    @commands.command()
    async def ping(self, ctx):
        """Returns the bot's response time."""

        pre_typing = time.monotonic()
        await ctx.trigger_typing()
        latency = int(round((time.monotonic() - pre_typing) * 1000))
        await ctx.send(ctx._("ping_response").format(latency))
