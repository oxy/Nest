"""
Provides cog for core moderator commands.
"""
from discord.ext import commands


class ModCommands:
    @commands.command()
    @commands.has_permissions(manage_server=True)
    @commands.guild_only()
    async def setprefix(self, ctx, category: str, prefix: str):
        """
        Set a prefix for a category.
        """
        if category not in ["user", "mod"]:
            # TODO: implement suggested arguments.
            await ctx.send(ctx._("prefix_invalid_category").format(category))
            return

        prefixes = ctx.prefixes.copy()
        prefixes.update({category: prefix})

        await ctx.bot.providers["prefix"].set()
        await ctx.send(
            ctx._("prefix_set_success").format(
                category=category, prefix=prefix
            )
        )
