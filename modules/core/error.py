"""
Provide a default error handler that logs errors to Discord.
"""
import functools
import math
import sys
import traceback

from discord.ext import commands

import nest


class ErrorHandler(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """
        Handle an exception raised by a command.
        Handle expected exceptions first, then log to console.

        Parameters
        ----------
        ctx:
            Context in which the exception occured.
        exception:
            The CommandInvokeError that was raised.
        """

        if not hasattr(ctx, '_'):
            traceback.print_exception(type(error), error, error.__traceback__)
            return

        ctx._ = functools.partial(ctx._, cog="ErrorHandler")
        error = getattr(error, 'original', error)
        etype = type(error)

        if isinstance(error, commands.CommandNotFound):
            # Ignore Command Not Found
            return

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(ctx._("cooldown").format(math.ceil(error.retry_after)))

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(ctx._("disabled"))

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(ctx._("missing_arg").format(error.param.name))

        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send(ctx._("nsfw_required"))

        elif etype in nest.exceptions.EXC_I18N_MAP:
            await ctx.send(
                ctx._(nest.exceptions.EXC_I18N_MAP[etype]).format(**error.__dict__)
            )

        elif isinstance(error, commands.CommandError):
            await ctx.send(str(error))

        else:
            lines = traceback.format_exception(etype, error, error.__traceback__)
            error_tb = "".join(lines)
            print(ctx._)
            await ctx.send(ctx._("unknown_error").format(f"```py\n{error_tb}```"))

            print(error_tb, file=sys.stderr)
