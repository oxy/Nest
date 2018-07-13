"""
Provides informational commands.

:copyright: (c) 2017 Jakeoid, 2018 n303p4.
:license: MIT, see LICENSE.md for details.
"""

import sys
import datetime

import discord
from discord.ext import commands


class InfoCommands:
    @commands.command()
    async def info(self, ctx):
        """Display information about Birb"""

        embed = discord.Embed()

        fields = {
            ctx._("servers"): f"{len(ctx.bot.guilds)}",
            ctx._("users"): f"{sum(m for m in ctx.bot.get_all_members())}",
            ctx._("bot_users"): f"{sum(m for m in ctx.bot.get_all_members() if m.bot)}",
            ctx._("human_users"): f"{sum(m for m in ctx.bot.get_all_members() if not m.bot)}",
            ctx._("discord_py"): f"{discord.__version__}",
            ctx._("python"): ".".join(str(e) for e in sys.version_info[:3]),
            ctx._("website"): "**[birb.pw](https://birb.pw/)**",
            ctx._("invite"): "**[invite.birb.pw](https://invite.birb.pw)**",
            ctx._("support"): "**[discord.gg/BysDKDB](https://discord.gg/BysDKDB)**",
            ctx._("library"): "**[discord.py](https://github.com/Rapptz/discord.py)**",
        }

        for name, value in fields.items():
            embed.add_field(name=name, value=value, inline=True)

        embed.set_author(icon_url=ctx.bot.user.avatar_url,
                         name=ctx.bot.user.name,
                         url="http://birb.pw/")
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)

        await ctx.send(embed=embed)
