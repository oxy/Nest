"""
RNG commands.
"""

import random
from discord.ext import commands

AAA = ("a", "A")


class RandomCommands(commands.Cog):
    """Commands that produce a random text output."""

    @commands.command(aliases=["coinflip"])
    async def coin(self, ctx):
        """Flip a coin."""

        choice = random.choice(["heads", "tails"])
        await ctx.send(ctx._(choice))

    @commands.command(aliases=["diceroll"])
    async def dice(self, ctx, diceroll: str = "1d6"):
        """Roll a die wiith input in the AdX notation."""

        times, num = diceroll.split("d")
        times = int(times) if times else 1
        num = int(num) if num else 6
        maxscore = times * num
        score = random.randint(times, maxscore)
        await ctx.send(
            ctx._("roll_result").format(score=score, maxscore=maxscore)
        )

    @commands.command()
    async def rate(self, ctx, *, content: str):
        """Gives something a rating."""

        num = random.randint(0, 10)
        await ctx.send(ctx._("rating").format(content=content, rating=num))

    @commands.command(name="8ball")
    async def eightball(self, ctx):
        """Asks the magic 8ball a question."""
        await ctx.send(random.choice(ctx._("8ball")))

    @commands.command(aliases=("a", "aa"))
    async def aaa(self, ctx):
        """AAAAAAA!"""
        await ctx.send(random.choice(AAA) * random.randint(1, 200))
