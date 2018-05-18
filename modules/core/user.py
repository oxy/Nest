"""
Provides core user-facing features, such as ping.
"""

import time
from discord.ext import commands


class UserCommands:
    category = "user"

    @commands.command()
    async def ping(self, ctx):
        """Returns the bot's response time."""

        pre_typing = time.monotonic()
        await ctx.trigger_typing()
        latency = int(round((time.monotonic() - pre_typing) * 1000))
        await ctx.send(ctx._("ping_response").format(latency))

    @commands.group()
    async def locale(self, ctx) -> None:
        """List locales and get current locale."""

        if ctx.invoked_subcommand:
            return
        text = ctx._("locale").format(ctx.locale)
        text += "\n```yml\n"
        for loc, names in ctx.bot.i18n.locales(ctx.locale).items():
            text += f"{loc}: "
            if names["user"] == names["native"]:
                text += names["user"] + "\n"
            else:
                text += f"{names['user']} - {names['native']}\n"
        text += "```"
        await ctx.send(text)

    @locale.command(name="set")
    async def set_locale(self, ctx, locale: str) -> None:
        """Set a locale."""

        if not ctx.bot.i18n.is_locale(locale):
            await ctx.send(ctx._("locale_invalid").format(locale))
            return

        await ctx.bot.providers['locale'].set(ctx, locale)
        await ctx.send(ctx._("locale_success", locale=locale).format(locale))

    @commands.command(aliases=["whatprefix"])
    async def prefix(self, ctx, *_):
        """
        Get the bot's current prefixes.
        """
        message = "```yml\n"
        for key, prefix in ctx.prefixes:
            key = ctx._(f"prefix_{key}") 
            message += f"{key}: {prefix}"
        message += "```"
        await ctx.send(message)
