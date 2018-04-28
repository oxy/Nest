'''
Set and display user locales.
'''

import discord
from discord.ext import commands

async def get_locale(bot, user: discord.User) -> str:
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
        Locale of the user.
    '''
    async with bot.database.acquire() as conn:
        locale = await conn.fetchval(
            'SELECT locale FROM locale WHERE id=$1''', user.id)
    return locale


class Locale():
    '''Locale cog.'''
    category = 'user'
    requires = ['database']
    provides = {'locale': get_locale}

    @commands.group()
    async def locale(self, ctx) -> None:
        '''List locales and get current locale.'''
        if ctx.invoked_subcommand:
            return
        text = ctx._('locale').format(ctx.locale)
        text += '\n```yml\n'
        for loc, names in ctx.bot.i18n.locales(ctx.locale).items():
            text += f'{loc}: '
            if names['user'] == names['native']:
                text += names['user'] + '\n'
            else:
                text += f"{names['user']} - {names['native']}\n"
        text += '```'
        await ctx.send(text)

    @locale.command(name='set')
    async def set_locale(self, ctx, locale: str) -> None:
        '''Set a locale.'''

        if not ctx.bot.i18n.is_locale(locale):
            await ctx.send(ctx._('locale_invalid').format(locale))
            return

        async with ctx.bot.database.acquire() as conn:
            await conn.execute('''
                INSERT INTO locale (id, locale) VALUES ($1, $2) ON CONFLICT (id)
                DO UPDATE SET (id, locale) = ($1, $2);
            ''', ctx.author.id, locale)

        await ctx.send(ctx._('locale_success', locale=locale).format(locale))

def setup(bot):
    bot.add_cog(Locale())
