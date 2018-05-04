import discord
from discord.ext import commands

from nest import exceptions

FIELDS = {
    "rating": "averageRating", "status": "status", "started": "startDate"
}


class KitsuWrapper:
    category = "user"

    @commands.command(aliases=["manga", "anime"])
    async def kitsu(self, ctx, *, name: str):
        """
        Get manga or anime from kitsu.io
        """
        req = "anime" if ctx.invoked_with == "kitsu" else ctx.invoked_with
        url = f"https://kitsu.io/api/edge/{req}"
        params = {"filter[text]": name, "page[limit]": 1}
        async with ctx.bot.session.get(url, params=params) as resp:
            if not resp.status == 200:
                raise exceptions.WebAPIInvalidResponse(
                    api="kitsu", status=resp.status
                )

            data = await resp.json(content_type="application/vnd.api+json")

        if not data["meta"]["count"]:
            raise exceptions.WebAPINoResults(api="kitsu")

        attributes = data["data"][0]["attributes"]

        embed = discord.Embed(
            title=attributes["canonicalTitle"],
            url=f"https://kitsu.io/{req}/{attributes['slug']}",
            description=attributes["synopsis"],
        )

        for field, item in FIELDS.items():
            embed.add_field(name=ctx._(field), value=attributes[item])

        if attributes["endDate"]:
            embed.add_field(name=ctx._("enddate"), value=attributes["endDate"])

        embed.set_thumbnail(url=attributes["posterImage"]["original"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(KitsuWrapper())
