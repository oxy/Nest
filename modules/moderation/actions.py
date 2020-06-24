"""
Provides basic moderation actions.
"""

import discord
from discord.ext import commands

class ModActions(commands.Cog):
    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, user: discord.Member, reason: str = None):
        """
        Bans a member for a given reason.
        """

        if ctx.guild.roles.index(ctx.author.top_role) < \
                ctx.guild.roles.index(user.top_role) or \
                ctx.author is ctx.guild.owner:
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(ctx._("ban_success").format(str(user)))
        else:
            await ctx.send(ctx._("ban_failure").format(str(user)))

    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def softban(self, ctx, user: discord.Member, reason: str = None):
        """
        Softbans a member for a given reason to clear messages.
        """

        if ctx.guild.roles.index(ctx.author.top_role) < \
                ctx.guild.roles.index(user.top_role) or \
                ctx.author is ctx.guild.owner:
            await ctx.guild.ban(user, reason=reason)
            await ctx.guild.unban(user)
            await ctx.send(ctx._("softban_success").format(str(user)))
        else:
            await ctx.send(ctx._("softban_failure").format(str(user)))

    @commands.command()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, user: discord.Member, reason: str = None):
        """
        Kicks a member for a given reason.
        """

        if ctx.guild.roles.index(ctx.author.top_role) < \
                ctx.guild.roles.index(user.top_role) or \
                ctx.author is ctx.guild.owner:
            await ctx.guild.kick(user, reason=reason)
            await ctx.send(ctx._("kick_success").format(str(user)))
        else:
            await ctx.send(ctx._("kick_failure").format(str(user)))


