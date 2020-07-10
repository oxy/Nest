from discord.ext import commands


class PrefixManager(commands.Cog):
    @commands.command(aliases=["whatprefix"])
    async def prefix(self, ctx, *_):
        """Get the current prefix."""

        prefix = await ctx.bot.get_cog("PrefixStore").get(ctx.message)
        await ctx.send(ctx._("current_prefix").format(prefix=prefix))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def setprefix(self, ctx, prefix: str):
        """Set a prefix for a guild."""

        await ctx.bot.get_cog("PrefixStore").set(ctx, prefix)
        await ctx.send(ctx._("prefix_set_success").format(prefix=prefix))
