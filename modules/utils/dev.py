"""
Commands to look up developer resources.
"""

import discord
from discord.ext import commands

from nest import exceptions, helpers

URL_PYPI_API = "https://pypi.python.org/pypi/{package}/json"
URL_PYPI_PACKAGE = "https://pypi.python.org/pypi/{package}"
FIELDS_PYPI = {"license", "docs_url", "home_page", "requires_python", "author"}


class PackageLookups:
    category = "user"

    @commands.command()
    async def pypi(self, ctx, package: str):
        """
        Look up a package on the Python Package Index.
        """
        data_url = URL_PYPI_API.format(package=package)

        async with ctx.bot.session.get(data_url) as resp:
            if not resp.status in [200, 404]:
                raise exceptions.WebAPIInvalidResponse(
                    api="PyPI", status=resp.status
                )

            if resp.status == 404:
                await ctx.send("{package} isn't a package on PyPI!")
                return

            data = await resp.json()

        info = data["info"]

        embed = discord.Embed(
            title=f"{info['name']} `({info['version']})`",
            description=helpers.smart_truncate(info["description"]),
            url=URL_PYPI_PACKAGE.format(package=package),
        )

        for field in FIELDS_PYPI & info.keys():
            if info[field]:
                embed.add_field(name=ctx._(field), value=info[field])

        embed.set_thumbnail(url="http://i.imgur.com/1Pp5s56.png")
        await ctx.send(embed=embed)
