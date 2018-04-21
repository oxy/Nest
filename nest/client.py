'''
Provides the Nest client class.
'''

import functools
import logging

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands.view import StringView
import rethinkdb as r

from nest import db, i18n


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
    default_prefix: dict
        Default prefixes for each category.
    i18n: nest.i18n.I18n
        Internationalization functions for the bot.
    """
    def __init__(self, settings, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        # Initialize instances that need the asyncio loop
        dbconn = self.loop.run_until_complete(r.connect())
        self.database = db.DBWrapper(settings.get('database'), dbconn)
        self.session = aiohttp.ClientSession(loop=self.loop)

        self._logger = logging.getLogger('NestClient')
        self.owners = settings.get('owners')
        self.default_prefix = settings.get('prefixes')
        self.i18n = i18n.I18n(locale='en_US')

    async def on_ready(self):
        '''Log successful login event'''
        self._logger.info(
            f"Logged in as {self.user.name}. ID: {str(self.user.id)}")

        # Set the game.
        await self.change_presence(activity=discord.Activity(name="with code"))

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

        data = await self.database.read(
            table='guilds',
            itemid=message.guild.id,
            item='prefixes')

        if data is None:
            data = {}
        prefixes = {**self.default_prefix, **data}

        for category, prefix in prefixes.items():
            if view.skip_string(prefix):
                invoker = view.get_word()
                command = self.all_commands.get(invoker)
                if command and command.instance.category == category:
                    ctx.command = command
                    ctx.invoked_with = invoker
                    ctx.prefix = prefix
                break

        locale = await self.database.read(
            table='users',
            itemid=message.author.id,
            item='locale')

        ctx.locale = locale

        if ctx.command:
            ctx._ = functools.partial(
                self.i18n.getstr, locale=locale,
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
