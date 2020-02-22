"""
Provides the fakegit command.
"""

import discord
from discord.ext import commands

from nest import exceptions

WHATTHECOMMIT_API_URL = "http://whatthecommit.com/index.json"


class DeveloperFun(commands.Cog):
    """Developer humor (or lack thereof)."""

    @commands.command()
    async def fakegit(self, ctx):
        """Generates a fake commit message like a Discord webhook otherwise would."""

        async with ctx.bot.session.get(WHATTHECOMMIT_API_URL) as resp:
            if resp.status != 200:
                raise exceptions.WebAPIInvalidResponse(
                    api="whatthecommit", status=resp.status
                )
            data = await resp.json()

        guild = ctx.guild.name.lower().replace(" ", "_")
        channel = ctx.channel.name.lower().replace(" ", "_")

        embed = discord.Embed(
            title=f"[{guild}:{channel}] 1 new commit",
            description=f"[`{data['hash'][:8]}`]({data['permalink']}) {data['commit_message']}",
            url=data["permalink"],
        )

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
