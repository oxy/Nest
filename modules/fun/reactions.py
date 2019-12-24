import discord
from discord.ext import commands

from nest import exceptions

WEEBSH_API = "https://api.weeb.sh/images/random"

CATEGORIES = (
    "cry",
    "dance",
    "happy",
    "hug",
    "kiss",
    "lewd",
    "neko",
    "owo",
    "pat",
    "slap",
    "smug",
    "triggered",
)


def gen_command(category: str):
    """
    Generates a command.
    """

    @commands.command(
        name=category, help=f"Show a random anime {category} image.",
    )
    async def image(self, ctx):
        """[)
        Image search command, common for all categories.
        """
        async with ctx.bot.session.get(
            WEEBSH_API, params={"type": category}, headers=self._headers
        ) as resp:
            if not resp.status == 200:
                raise exceptions.WebAPIInvalidResponse(
                    api="weeb.sh", status=resp.status
                )

            data = await resp.json()  # some APIs don't set it
            img = data["url"]

        embed = discord.Embed()
        embed.set_image(url=img)
        embed.set_footer(
            text=ctx._("provided_by {service}").format(service="weebsh")
        )
        await ctx.send(embed=embed)

    return image


class _ReactionImages:
    def __init__(self, bot):
        self._headers = {"Authorization": bot.tokens["weebsh"]}


for c in CATEGORIES:
    setattr(_ReactionImages, c, gen_command(c))


class ReactionImages(_ReactionImages, commands.Cog):
    pass
