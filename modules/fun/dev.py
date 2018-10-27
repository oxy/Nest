"""
Provides the fakegit command.
"""

import discord
from discord.ext import commands

WHATTHECOMMIT_API_URL = "http://whatthecommit.com/index.json"


class DeveloperFun:
    category = "user"

    @commands.command()
    async def fakegit(self, ctx):
        """
        Generates a fake commit message like a Discord webhook otherwise would.
        """

        async with ctx.bot.session.get() as resp:
            data = await resp.json()

        guild = ctx.guild.name.lower().replace(" ", "_")
        channel = ctx.channel.name.lower().replace(" ", "_")

        embed = discord.Embed(
            title=f"[{guild}:{channel}] 1 new commit",
            description=f"[`{data['hash']}`]({data['permalink']}) {data['commit_message']}",
            url=data["permalink"],
        )

        embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar_url)

        await ctx.send(embed=embed)
