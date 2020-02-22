from urllib.parse import urlparse

import discord
from discord.ext import commands

from nest import exceptions

SERVICES = {
    "dog": ("https://random.dog/woof.json", "url"),
    "birb": ("https://random.birb.pw/tweet.json", "file"),
    "cat": ("https://nekos.life/api/v2/img/meow", "url"),
}

ALIASES = {
    "birb": ("randombirb", "bird", "randombird"),
    "cat": ("randomcat",),
    "dog": ("randomdog",),
}

INSPIROBOT_URL = "http://inspirobot.me/api?generate=true"

TEXT = {"birb": "https://random.birb.pw/img/"}


def gen_command(service: str, url: str, key: str):
    """
    Generates a command helper.
    """

    @commands.command(
        name=service,
        aliases=ALIASES.get(service, tuple()),
        help=f"Search {service} for images.",
    )
    async def image(self, ctx):
        """
        Image search command, common for all APIs.
        """
        async with ctx.bot.session.get(url) as resp:
            if not resp.status == 200:
                raise exceptions.WebAPIInvalidResponse(
                    api=service, status=resp.status
                )

            data = await resp.json(content_type=None)  # some APIs don't set it
            img = TEXT.get(service, "") + data[key]

        embed = discord.Embed()
        embed.set_image(url=img)
        embed.set_footer(
            text=ctx._("provided_by {service}").format(
                service=urlparse(url).netloc
            )
        )
        await ctx.send(embed=embed)

    return image


class _RandomImages:
    @commands.command(aliases=["inspirobot", "inspire"])
    async def inspiro(self, ctx):
        """
        Generates a random inspiring image for you!
        """
        async with ctx.bot.session.get(INSPIROBOT_URL) as resp:
            if resp.status != 200:
                raise exceptions.WebAPIInvalidResponse(
                    api="inspirobot", status=resp.status
                )
            url = await resp.text()

        embed = discord.Embed()
        embed.set_image(url=url)
        embed.set_footer(
            text=ctx._("provided_by {service}").format(service="inspirobot.me")
        )

        await ctx.send(embed=embed)


for sv, params in SERVICES.items():
    setattr(_RandomImages, sv, gen_command(sv, *params))


class RandomImages(_RandomImages, commands.Cog):
    pass
