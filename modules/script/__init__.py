import asyncio
import random
import inspect

import async_timeout
import arpeggio
from arpeggio import cleanpeg
import discord
from discord.ext import commands

from .interpreter import InterpreterPool
from . import exceptions, stdlib, parser


class Scripter:
    """
    Runner for NestScript.
    """

    category = "user"
    requires = ["database"]

    def __init__(self):
        protected = [f for _, f in inspect.getmembers(stdlib) if callable(f)]

        module_list = [random, int, float, str, dict, list, max, min, sum]
        modules = {m.__name__: m for m in module_list}

        self.interpreter = InterpreterPool(modules, protected)

    @commands.command()
    async def interpret(self, ctx, *, script):
        script = self.cleanup_code(script)
        ast = parser.parse(script)
        ctx.messages = []

        try:
            async with async_timeout.timeout(5):
                await self.interpreter.interpret(ctx, ast)
        except exceptions.ProtectionError:
            try:
                await ctx.channel.delete_messages(ctx.messages)
            except discord.Forbidden:
                tasks = [message.delete() for message in ctx.messages]
                await asyncio.gather(*tasks)
            raise

    @staticmethod
    def cleanup_code(body):
        # remove ```py\n```
        if body.startswith("```") and body.endswith("```"):
            return "\n".join(body.split("\n")[1:-1])

        # remove `foo`
        return body.strip("` \n")


def setup(bot):
    bot.add_cog(Scripter())
