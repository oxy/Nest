from discord.ext import commands

async def get_prefix(bot, message):
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
                '''SELECT user_prefix, mod_prefix FROM prefix WHERE id=$1''',
                message.guild.id)

        if prefixes:
            prefixes = dict(prefixes)
            return {k.split('_')[0]: v for k, v in prefixes.items()}

    else:
        return {}


class GuildPrefix:
    category = 'mod'
    requires = ['database']
    provides = {'prefix': get_prefix}

    @commands.group()
    async def prefix(self, ctx):
        # TODO: implement current prefix.
        pass

    @prefix.command(name='set')
    @commands.guild_only()
    async def set_prefix(self, ctx, category: str, prefix: str):
        # TODO: implement permission checks.
        if category not in ['user', 'mod']:
            # TODO: implement suggested arguments.
            await ctx.send(ctx._('invalid_category').format(category))
            return

        prefixes = ctx.prefixes.copy()
        prefixes.update({category: prefix})

        async with ctx.bot.database.acquire() as conn:
            await conn.execute('''
                INSERT INTO prefix (id, user_prefix, mod_prefix)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (id) DO UPDATE
                        SET (id, user_prefix, mod_prefix) = ($1, $2, $3);
            ''', ctx.guild.id, prefixes['user'], prefixes['mod'])

        await ctx.send(ctx._('set_success').format(
            category=category, prefix=prefix))


def setup(bot):
    bot.add_cog(GuildPrefix())
