'''
Set and display user locales.
'''

from discord.ext import commands
from nest import helpers

class Locale(helpers.cog('user')):
    '''Locale cog.'''
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
        # TODO: Verify if locale is valid.
        await ctx.bot.database.write(
            table='users',
            itemid=ctx.author.id,
            item='locale',
            data=locale)
        await ctx.send(ctx._('locale_success', locale=locale).format(locale))

def setup(bot):
    bot.add_cog(Locale())
