"""
Commands for fun text manipulation.
"""
import string

import discord
from discord.ext import commands

XD = """```
{word}           {word}     {word}  {word}
  {word}       {word}       {word}     {word}
    {word}   {word}         {word}      {word}
    {word}   {word}         {word}      {word}
  {word}       {word}       {word}     {word}
{word}           {word}     {word}  {word}
```"""

class TextManipulation(commands.Cog):
    """Manipulate text in funny ways."""

    def _create_embed(self, author: discord.User):
        embed = discord.Embed()
        embed.set_footer(text=author.name, icon_url=author.avatar_url)
        return embed

    @commands.command()
    async def bigtext(self, ctx, *, text: str):
        """Convert text into huge emoji."""

        table = str.maketrans({x: f":regional_indicator_{x.lower()}:" for x in string.ascii_letters})
        res = text.translate(table)
        await ctx.send(res, embed=self._create_embed(ctx.author))

    @commands.command()
    async def xd(self, ctx, *, word: str):
        """Make an XD out of the word given."""

        await ctx.send(XD.format(word=word), embed=self._create_embed(ctx.author))

    @commands.command()
    async def clapify(self, ctx, *, text: str):
        """Add clap emojis after each word."""
        res = " 👏 ".join(text.split())
        await ctx.send(res, embed=self._create_embed(ctx.author))

    @commands.command()
    async def tobleflep(self, ctx):
        pass

