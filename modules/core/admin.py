import traceback
import time
import textwrap

import discord

from discord.ext import commands

HASTE_POST_URL = "https://hastebin.com/documents/"
HASTE_URL = "https://hastebin.com/{key}.py"


class AdminCommands(commands.Cog):
    def __init__(self):
        self._eval = {
            "env": {},
            "count": 0
        }

    @commands.is_owner()
    @commands.group()
    async def module(self, ctx):
        pass
        
    @module.command()
    async def reload(self, ctx, module: str):
        ctx.bot.reload_module(module)
        await ctx.send(f"Successfully reloaded {module}!")
    
    @commands.is_owner()
    @module.command()
    async def load(self, ctx, module: str):
        ctx.bot.load_module(module)
        await ctx.send(f"Successfully loaded {module}!")

    @commands.is_owner()
    @commands.command(usage='<code>')
    async def eval(self, ctx, *, code: str):
        await ctx.trigger_typing()
        env = self._eval['env']
        env.update({'ctx': ctx})

        # Unwrap formatting and construct function
        code = code.replace('```py\n', '').replace('```', '').replace('`', '')
        fn = \
f"""
async def func(env):
    try:
        {textwrap.indent(code, ' '*8)}
    finally:
        env.update(locals())
"""
        before = time.monotonic()

        try:
            # Evaluate the function, with given global env, then await it
            exec(fn, env)
            func = env['func']
            output = await func(env)
            if output is not None:
                output = repr(output)
        except Exception as e:
            output = f'{type(e).__name__}: {e}'

        after = time.monotonic()
        self._eval['count'] += 1
        count = self._eval['count']
        lines = code.split('\n')

        if len(lines) == 1:
            in_ = f'In [{count}]: {lines[0]}'
        else:
            prefix = f'In [{count}]: '
            first_line = f'{prefix}{lines[0]}'
            rest = '\n'.join(lines[1:])
            rest = textwrap.indent(rest, '...: '.rjust(len(prefix)))
            in_ = 'In [{}]: {}\n{}'.format(count, first_line, rest)

        message = '```py\n{}'.format(in_)
        ms = int(round((after - before) * 1000))

        if output is not None:
            message += '\nOut[{}]: {}'.format(count, output)

        if ms > 100:  # noticeable delay
            message += '\n# {} ms\n```'.format(ms)
        else:
            message += '\n```'

        try:
            await ctx.send(message)
        except discord.HTTPException:
            async with ctx.bot.session.post(HASTE_POST_URL, data=message) as resp:
                # TODO: handle error, raise WebAPIException
                data = await resp.json()

            await ctx.send(HASTE_URL.format(key=data["key"]))

    @commands.is_owner()
    @commands.command()
    async def reset_eval(self, ctx):
        self._eval = {
            "env": {},
            "count": 0
        }
        await ctx.send(ctx._("eval_reset"))
