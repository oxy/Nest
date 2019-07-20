"""
RNG commands.
"""

import random
from discord.ext import commands


class RandomCommands(commands.Cog):    
    @commands.command(aliases=["coinflip"])
    async def coin(self, ctx):
        """
        Flips a coin randomly and gives you the result.
        """

        choice = random.choice(["heads", "tails"])
        await ctx.send(ctx._(choice))

    @commands.command(aliases=["diceroll"])
    async def dice(self, ctx, diceroll: str = '1d6'):
        """
        Rolls a die wiithh input in the AdX notation.
        """
        times, num = diceroll.split('d')
        times = int(times) if times else 1
        num = int(num) if num else 6
        maxscore = times*num
        score = random.randint(times, maxscore)
        await ctx.send(ctx._("roll_result").format(score=score, maxscore=maxscore))
        

    @commands.command()
    async def rate(self, ctx, *args):
        content = ' '.join(args)
        num = random.randint(0, 10)
        await ctx.send(ctx._("rating").format(content=content, num=num))

