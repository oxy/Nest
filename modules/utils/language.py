"""
Provides language commands.

:copyright: (c) 2017 Jakeoid, 2018 n303p4.
:license: MIT, see LICENSE.md for details.
"""

import json

import discord
from discord.ext import commands

from nest import exceptions


API_JISHO_ORG = "http://jisho.org/api/v1/search/words?keyword={0}"
API_URBAN_DICTIONARY = "http://api.urbandictionary.com/v0/define"


class LanguageCommands:
    category = "user"

    @commands.command()
    async def jisho(self, ctx, *, word: str):
        """Translate a word into Japanese."""
        url = API_JISHO_ORG.format(word)
        headers = {"Content-type": "application/json"}

        async with ctx.bot.session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.text()
                response = json.loads(data)
            else:
                raise exceptions.WebAPIInvalidResponse(
                    api="jisho", status=response.status
                )

        data = response["data"][0]

        japanese = data["japanese"][0]
        senses = data["senses"][0]["english_definitions"]

        title = japanese.get("word", "???")
        reading = japanese.get("reading", "???")

        embed = discord.Embed(title=title, description=reading)

        embed.add_field(name=ctx._("english"), value=", ".join(senses))

        try:
            speech = data["senses"][0]["parts_of_speech"][0]
            embed.set_footer(text=speech or "???")
        except (KeyError, IndexError):
            speech = None

        await ctx.send(embed=embed)

    @commands.command(aliases=["urbandictionary"])
    async def urban(self, ctx, *, word: str):
        """Grab a word from urban dictionary."""

        params = {"term": word}
        async with ctx.bot.session.get(API_URBAN_DICTIONARY, params=params) as response:
            if response.status == 200:
                data = await response.text()
                response = json.loads(data)
            else:
                raise exceptions.WebAPIInvalidResponse(
                    api="urbandictionary.com", status=response.status
                )

        try:
            content = response["list"][0]
        except (KeyError, IndexError):
            raise exceptions.WebAPINoResults(api="urbandictionary.com")

        thumbs_up = content["thumbs_up"]
        thumbs_down = content["thumbs_down"]

        embed = discord.Embed(title=content["word"], description=content["author"],
                              url=content["permalink"])

        if "definition" in content:
            embed.add_field(name=ctx._("definition"), value=content["definition"], inline=False)

        if "example" in content:
            embed.add_field(name=ctx._("example"), value=content["example"], inline=False)

        embed.add_field(name=ctx._("upvotes"),
                        value=f":thumbsup::skin-tone-2: {thumbs_up}",
                        inline=True)
        embed.add_field(name=ctx._("downvotes"),
                        value=f":thumbsdown::skin-tone-2: {thumbs_down}",
                        inline=True)

        await ctx.send(embed=embed)
