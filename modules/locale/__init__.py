'''
Set and display user locales.
'''

from discord.ext import commands

class Locale():
    '''Locale cog.'''
    category = 'user'

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
        async with ctx.bot.database.acquire() as conn:
            await conn.execute('''
                INSERT INTO locale (id, locale) VALUES ($1, $2) ON CONFLICT DO UPDATE
            ''', ctx.user.id, locale)

        await ctx.send(ctx._('locale_success', locale=locale).format(locale))

def setup(bot):
    bot.add_cog(Locale())
