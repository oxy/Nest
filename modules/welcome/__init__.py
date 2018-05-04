import re
import discord
from discord.ext import commands


class Welcomer():
    category = "mod"
    requires = ["database"]
    provides = {}

    def __init__(self):
        self.regex = re.compile(r"<#(\d+)>|$")

    @commands.command()
    @commands.guild_only()
    async def welcome(self, ctx, channel: str, *, message: str):
        """
        Set welcome channel (leave blank for nothing) and message.
        """
        if channel == "DM":
            channelid = 0
        else:
            matches = self.regex.findall(channel)
            if matches:
                channelid = matches[0]
            else:
                raise ValueError

        async with ctx.bot.database.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO welcome (id, message, channel) VALUES ($1, $2, $3) ON CONFLICT DO UPDATE
            """,
                ctx.guild.id,
                message,
                channelid,
            )
        await ctx.send("welcome_success")

    @staticmethod
    async def send_welcome(bot, member: discord.Member):
        """
        Send a welcome message.

        Parameters
        -----------
        bot: nest.client.NestClient:
            The Nest client.
        member: discord.Member:
            The new member that joined the guild.
        """
        async with bot.database.acquire() as conn:
            welcome = await conn.fetchrow(
                """SELECT (id, message, channel) IN welcome WHERE id=$1""",
                member.guild.id,
            )
        if not welcome:
            return
        if welcome["channel"]:
            channel = bot.get_channel(welcome["channel"])
        else:
            channel = bot.get_channel(member.id)
        await channel.send(welcome["message"].format(member.mention))


def setup(bot):
    """Add cog and listener"""
    bot.add_cog(Welcomer())
    bot.add_listener(Welcomer.send_welcome, "on_member_join")
