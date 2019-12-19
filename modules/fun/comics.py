"""
Commands to search for comics.
"""

import discord
from discord.ext import commands

from nest import exceptions


class Comics(commands.Cog):
    @commands.command()
    async def xkcd(self, ctx, number: int = None):
        """
        Grabs a (or the latest) comic from xkcd and shows it.
        """

        if number:
            url = f"https://xkcd.com/{number}/info.0.json"
        else:
            url = f"https://xkcd.com/info.0.json"

        async with ctx.bot.session.get(url) as resp:
            if resp.status not in [200, 404]:
                raise exceptions.WebAPIInvalidResponse(
                    api="xkcd", status=resp.status
                )

            if resp.status == 404:
                await ctx.send(ctx._("not_a_comic").format(num=number, comic="XKCD"))
                return

            data = await resp.json()

        number = data["num"]
        image = data["img"]
        title = data["safe_title"]
        day = data["day"]
        month = data["month"]
        year = data["year"]

        link = f"https://xkcd.com/{number}"

        embed = discord.Embed(title=f"{number} - **{title}**", url=link)
        embed.set_footer(text=ctx._("published") + f"{year}{month}{day}")
        embed.set_image(url=image)

        await ctx.send(embed=embed)
