"""
Provides the Nest client class.
"""

import asyncio
import functools
import logging
from datetime import datetime
from typing import Dict, Any

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands.view import StringView

from nest import i18n, exceptions


class PrefixGetter:
    def __init__(self, default: str):
        self._default = default

    async def __call__(self, bot, message: discord.Message):
        """|coro|

        Retrieves the prefix the bot is listening to
        with the message as a context.

        Parameters
        -----------
        ctx: :class:`commands.Context`
            The context to get the prefix of.

        Returns
        --------
        Dict[str, str]
            A prefix the bot is listening for in each category.
        """
        cog = bot.get_cog("PrefixStore")
        if cog:
            prefix = cog.get(message)
            if asyncio.iscoroutine(prefix):
                prefix = await prefix

        if not isinstance(prefix, str):
            prefix = self._default

        return commands.when_mentioned_or(prefix)(bot, message)

async def get_locale(bot, ctx: commands.Context):
    """|coro|

    Retrieves the locale of a user to respond with.

    Parameters
    -----------
    ctx: :class:`commands.Context`
        The context to get the prefix of.

    Returns
    -------
    str:
        Locale to use in responses.
    """
    cog = bot.get_cog("LocaleStore")

    if cog:
        ret = cog.get(ctx)
        if asyncio.iscoroutine(ret):
            ret = await ret
        return ret


class NestClient(commands.AutoShardedBot):
    """Main client for Nest.

    Attributes
    ----------
    session: aiohttp.ClientSession
        aiohttp session to use for making requests.
    tokens: Dict[str, str]
        Tokens passed to the bot.
    created: datetime.datetime()
        Time when bot instance was initialised.
    i18n: nest.i18n.I18n
        Internationalization functions for the bot.
    """

    def __init__(self, **options):
        super().__init__(
            PrefixGetter(options.pop("prefix")),
            **options,
        )
        self._logger = logging.getLogger("NestClient")
        self.tokens: Dict[str, str] = options.pop("tokens", {})
        self.owner_ids = set(options.pop("owners", []))
        self.created = datetime.now()
        self.session = aiohttp.ClientSession(loop=self.loop)

        self.i18n = i18n.I18n(locale=options.pop("locale", "en_US"))
        self.options = options

    async def on_ready(self):
        """Log successful login event"""
        self._logger.info(
            f"Logged in as {self.user.name}. ID: {str(self.user.id)}"
        )

        # Set the game.
        await self.change_presence(activity=discord.Activity(name="with code"))

    async def get_context(
        self, message: discord.Message, *, cls=commands.Context
    ) -> commands.Context:
        """|coro|

        Returns the invocation context from the message.

        The returned context is not guaranteed to be a valid invocation
        context, :attr:`.Context.valid` must be checked to make sure it is.
        If the context is not valid then it is not a valid candidate to be
        invoked under :meth:`~.Bot.invoke`.

        Parameters
        -----------
        message: :class:`discord.Message`
            The message to get the invocation context from.
        cls
            The factory class that will be used to create the context.
            By default, this is :class:`.Context`. Should a custom
            class be provided, it must be similar enough to :class:`.Context`'s
            interface.

        Returns
        --------
        :class:`.Context`
            The invocation context. The type of this can change via the
            ``cls`` parameter.
        """
        ctx = await super().get_context(message, cls=cls)

        if ctx.command:
            user_locale = await get_locale(self, ctx)
            ctx.locale = user_locale if user_locale else self.i18n.locale
            ctx._ = functools.partial(
                self.i18n.getstr,
                locale=ctx.locale,
                cog=ctx.command.cog_name,
            )

        return ctx

    def load_module(self, name: str):
        """Loads a module from the modules directory.

        A module is a d.py extension that contains commands, cogs, or
        listeners and i18n data.

        Parameters
        ----------
        name: str
            The extension name to load. It must be a valid name of a folder
            within the modules directory.

        Raises
        ------
        ClientException
            The extension does not have a setup function.
        ImportError
            The extension could not be imported.
        """
        if name in self.extensions:
            return

        self.load_extension(f"modules.{name}")
        self.i18n.load_module(name)

    def reload_module(self, name: str):
        """Loads a module from the modules directory.

        A module is a d.py extension that contains commands, cogs, or
        listeners and i18n data.

        Parameters
        ----------
        name: str
            The extension name to load. It must be a valid name of a folder
            within the modules directory.

        Raises
        ------
        ClientException
            The extension does not have a setup function.
        ImportError
            The extension could not be imported.
        """

        self.reload_extension(f"modules.{name}")
        self.i18n.load_module(name)

    def run(self, bot: bool = True):
        """
        Start running the bot.
        
        Parameters
        ----------
        bot: bool
            If bot is a bot account or a selfbot.
        """
        super().run(self.tokens["discord"], bot=bot)
