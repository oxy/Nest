'''
Load and start the Nest client.
'''

import os
import logging
from typing import Dict

import discord
import yaml

from nest import client, helpers

DEFAULTS = {'prefix': {'user': 'nest$', 'mod': 'nest@', 'owner': 'nest#'},
            'database': 'nest', 'locale': 'en_US'}

def gen_prefix_callable(default_prefixes: dict):
    '''
    Generates a prefix callable.
    '''
    async def prefix(bot: client.NestClient,
                     message: discord.Message) -> Dict[str, str]:
        '''|coro|

        Returns a valid prefix when given a message.

        Parameters
        ----------
        bot: client.NestClient
            The bot instance (used for acquiring a database connection).
        message: discord.Message
            The message to get a prefix for.

        Returns
        -------
        Dict[str, str]
            Dictionary of prefixes per category.
        '''
        if message.guild:
            async with bot.database.acquire() as conn:
                prefixes = await conn.fetchrow(
                    '''SELECT (user, mod) FROM prefixes WHERE id=$1''',
                    message.guild.id)

            if prefixes is not None:
                return {**default_prefixes, **prefixes}
        else:
            return default_prefixes
    return prefix

async def gen_locale_callable(default_locale: str):
    '''
    Generates a locale callable.
    '''
    async def locale(bot: client.NestClient, user: discord.User) -> str:
        '''|coro|

        Returns a valid locale when given a user.

        Parameters
        ----------
        bot: client.NestClient
            The bot instance (used for acquiring a database connection).
        message: discord.Message
            The user to return a locale for.

        Returns
        -------
        str
            Dictionary of prefixes per category.
        '''
        async with bot.database.acquire() as conn:
            locale = await conn.fetchval(
                '''SELECT (locale) FROM locale WHERE id=$1''', user.id)
        return locale if locale else default_locale

    return locale

def main():
    '''
    Parse config from file or environment and launch bot.
    '''
    logger = logging.getLogger()
    if os.path.isfile('config.yml'):
        logger.debug('Found config, loading...')
        with open('config.yml') as file:
            config = yaml.safe_load(file)
    else:
        logger.debug('Config not found, trying to read from env...')
        env = {key[8:].lower(): val for key, val in os.environ.items()
               if key.startswith('NESTBOT_')}
        config = {'tokens': {}, 'settings': {}}

        for key, val in env.items():
            if key.startswith('token_'):
                basedict = config['tokens']
                keys = key[6:].split('_')
            else:
                basedict = config['settings']
                keys = key.split('_')

            pointer = helpers.dictwalk(
                dictionary=basedict,
                tree=keys[:-1],
                fill=True)

            if ',' in val:
                val = val.split(',')

            pointer[keys[-1]] = val

    settings = {**DEFAULTS, **config['settings']}
    prefixes = gen_prefix_callable(settings['prefix'])
    locale = gen_locale_callable(settings['locale'])

    bot = client.NestClient(
        database=settings['database'],
        locale=locale,
        prefix=prefixes,
        owners=settings['owners'])

    for module in os.listdir('modules'):
        # Ignore hidden directories
        if not module.startswith('.'):
            bot.load_module(module)

    bot.run(config['tokens']['discord'])


if __name__ == '__main__':
    main()
