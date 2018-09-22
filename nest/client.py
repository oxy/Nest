"""
Provides the Nest client class.
"""

import asyncio
import functools
import logging
from typing import Dict, Any

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands.view import StringView

from nest import i18n, exceptions, abc


class NestClient(commands.AutoShardedBot):
    """Main client for Nest.

    Attributes
    ----------
    database: asyncpg.pool.ConnectionPool
        The connection pool for the database.
    session: aiohttp.ClientSession
        aiohttp session to use for making requests.
    owners: list
        List of owners of the bot.
    i18n: nest.i18n.I18n
        Internationalization functions for the bot.
    """

    def __init__(self, settings: Dict[str, Any], tokens: Dict[str, str]):
        super().__init__(settings["prefix"])
        self._logger = logging.getLogger("NestClient")
        self.features = set()
        self.providers = {}
        self.tokens = tokens
        self.settings = settings

        database = settings.get("database", None)
        if database:
            import asyncpg

            self.database = self.loop.run_until_complete(
                asyncpg.create_pool(database=database, loop=self.loop)
            )
            self.features.add("database")
        else:
            self.database = None

        self.session = aiohttp.ClientSession(loop=self.loop)

        self.locale = settings.get("locale", "en_US")
        self.owners = settings["owners"]
        self.i18n = i18n.I18n(locale=self.locale)

    async def on_ready(self):
        """Log successful login event"""
        self._logger.info(
            f"Logged in as {self.user.name}. ID: {str(self.user.id)}"
        )

        # Set the game.
        await self.change_presence(activity=discord.Activity(name="with code"))

    async def get_prefix(self, ctx: commands.Context):
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
        prefixes = self.command_prefix
        provider = self.providers.get("prefix", None)

        ret = None
        if provider:
            ret = provider.get(ctx)
            if asyncio.iscoroutine(ret):
                ret = await ret
            if ret is not None:
                prefixes.update(ret)

        return prefixes

    async def get_locale(self, ctx: commands.Context):
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
        provider = self.providers.get("locale", None)

        ret = None
        if provider:
            ret = provider.get(ctx)
            if asyncio.iscoroutine(ret):
                ret = await ret

        return ret if ret else self.locale

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

        view = StringView(message.content)
        ctx = cls(prefix=None, view=view, bot=self, message=message)

        ctx.prefixes = await self.get_prefix(ctx)

        for category, prefix in ctx.prefixes.items():
            if view.skip_string(prefix):
                invoker = view.get_word()
                command = self.all_commands.get(invoker)
                if command and command.instance.category == category:
                    ctx.command = command
                    ctx.invoked_with = invoker
                    ctx.prefix = prefix
                break

        ctx.locale = await self.get_locale(ctx)

        if ctx.command:
            ctx._ = functools.partial(
                self.i18n.getstr,
                locale=ctx.locale,
                cog=type(ctx.command.instance).__name__,
            )

        return ctx

    async def is_owner(self, user: discord.User) -> bool:
        if user.id in self.owners:
            return True
        else:
            raise commands.NotOwner

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

    def add_provider(self, provider: abc.Provider):
        """Add a Provider to the bot.

        Parameters
        ----------
        provider: abc.Provider
            Provider to add to the bot.
        """
        self.providers[provider.provides] = provider

    def has_features(self, *features: str) -> bool:
        """
        Check if the bot instance has all listed features.
        """
        return set(features) <= self.features

    def run(self, bot: bool = True):
        """
        Start running the bot.
        
        Parameters
        ----------
        bot: bool
            If bot is a bot account or a selfbot.
        """
        super().run(self.tokens["discord"], bot=bot)
