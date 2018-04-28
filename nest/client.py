'''
Provides the Nest client class.
'''

import asyncio
import functools
import logging
from typing import List, Optional

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands.view import StringView

from nest import i18n, exceptions

class NestClient(commands.AutoShardedBot):
    """Main client for Nest.

    Attributes
    ----------
    database: nest.db.DBWrapper
        The wrapper for the database.
    session: aiohttp.ClientSession
        aiohttp session to use for making requests.
    owners: list
        List of owners of the bot.
    i18n: nest.i18n.I18n
        Internationalization functions for the bot.
    """
    def __init__(self, *, database: Optional[str] = None, locale: str,
                 prefix: str, owners: List[int]):
        super().__init__(prefix)
        self._logger = logging.getLogger('NestClient')
        self.features = set()
        self.providers = {}

        if database:
            import asyncpg
            self.database = self.loop.run_until_complete(asyncpg.create_pool(
                database=database, loop=self.loop))
            self.features.add('database')
        else:
            self.database = None

        self.session = aiohttp.ClientSession(loop=self.loop)

        self.locale = locale
        self.owners = owners
        self.i18n = i18n.I18n(locale='en_US')

    async def on_ready(self):
        '''Log successful login event'''
        self._logger.info(
            f"Logged in as {self.user.name}. ID: {str(self.user.id)}")

        # Set the game.
        await self.change_presence(activity=discord.Activity(name="with code"))

    async def get_prefix(self, message: discord.Message):
        """|coro|

        Retrieves the prefix the bot is listening to
        with the message as a context.

        Parameters
        -----------
        message: :class:`discord.Message`
            The message context to get the prefix of.

        Raises
        --------
        :exc:`.ClientException`
            The prefix was invalid. This could be if the prefix
            function returned None, the prefix list returned no
            elements that aren't None, or the prefix string is
            empty.

        Returns
        --------
        Dict[str, str]
            A prefix the bot is listening for in each category.
        """
        prefixes = self.command_prefix
        provider = self.providers.get('prefix', None)

        if provider:
            ret = provider(self, message)
            if asyncio.iscoroutine(ret):
                ret = await ret
            if ret is not None:
                prefixes.update(ret)

        return prefixes

    async def get_locale(self, user: discord.User):
        """|coro|

        Retrieves the locale of a user to respond with.

        Parameters
        -----------
        user: :class:`discord.User`
            The message context to get the prefix of.

        Returns
        -------
        str:
            Locale to use in responses.
        """
        provider = self.providers.get('locale', None)
        if provider:
            ret = provider(self, user)
            if asyncio.iscoroutine(ret):
                ret = await ret

        return ret if ret else self.locale

    async def get_context(
            self, message: discord.Message, *, cls=commands.Context):
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
        ctx = cls(prefix=None, view=view,
                  bot=self, message=message)

        ctx.prefixes = await self.get_prefix(message)

        for category, prefix in ctx.prefixes.items():
            if view.skip_string(prefix):
                invoker = view.get_word()
                command = self.all_commands.get(invoker)
                if command and command.instance.category == category:
                    ctx.command = command
                    ctx.invoked_with = invoker
                    ctx.prefix = prefix
                break

        ctx.locale = await self.get_locale(message.author)

        if ctx.command:
            ctx._ = functools.partial(
                self.i18n.getstr, locale=ctx.locale,
                cog=type(ctx.command.instance).__name__)

        return ctx

    async def is_owner(self, user: discord.User) -> bool:
        if user.id in self.owners:
            return True
        else:
            raise commands.NotOwner

    def load_module(self, name: str):
        '''Loads a module from the modules directory.

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
        '''
        if name in self.extensions:
            return

        self.load_extension(f'modules.{name}')
        self.i18n.load_module(name)

    def add_cog(self, cog):
        '''Adds a "cog" to the bot.

        A cog is a class that has its own event listeners and commands.

        They are meant as a way to organize multiple relevant commands
        into a singular class that shares some state or no state at all.

        The cog can have a ``requires`` list to list out any required
        features, and a ``provides`` dict that can provide functions to the bot.

        The cog can also have a ``__global_check`` member function that allows
        you to define a global check. See :meth:`.check` for more info. If
        the name is ``__global_check_once`` then it's equivalent to the
        :meth:`.check_once` decorator.

        More information will be documented soon.

        Parameters
        -----------
        cog
            The cog to register to the bot.
        '''
        required = getattr(cog, 'requires', [])
        unavailable = set(required) - self.features
        if unavailable:
            raise exceptions.MissingFeatures(cog, unavailable)
        super().add_cog(cog)

        provides = getattr(cog, 'provides', None)
        if provides:
            self.providers.update(cog.provides)

    def remove_cog(self, name):
        """Removes a cog from the bot.

        All registered commands, event listeners and providers that the
        cog has registered will be removed as well.

        If no cog is found then this method has no effect.

        If the cog defines a special member function named ``__unload``
        then it is called when removal has completed. This function
        **cannot** be a coroutine. It must be a regular function.

        Parameters
        -----------
        name : str
            The name of the cog to remove.
        """

        cog = self.cogs.pop(name, None)
        if not cog:
            return

        provides = getattr(cog, 'provides', {})
        for key, provider in provides.items():
            assert self.providers[key] is provider
            self.providers.pop(key)

        super().remove_cog(name)
