"""
Basic moderation utilities for Birb.
"""

import discord
from discord.ext import commands

MOD_EMOTICONS = {
    "online": "<:online2:464520569975603200>",
    "offline": "<:offline2:464520569929334784>",
    "idle": "<:away2:464520569862357002>",
    "dnd": "<:dnd2:464520569560498197>"
}

class CheckMods(commands.Cog):
    @commands.command(aliases=["staff"])
    async def mods(self, ctx):
        mods = [m for m in ctx.guild.members 
                if m.permissions_in(ctx.channel).ban_members and not m.bot]

        mods_by_status = {'online': [], 'offline': [], 'idle': [], 'dnd': []}
        
        for mod in mods:
            mods_by_status[str(mod.status)].append(mod)
        
        msg = ""

        for status in ['online', 'idle', 'dnd', 'offline']:
            if mods_by_status[status]:
                msg += MOD_EMOTICONS[status] + " " + \
                    ", ".join(str(mod) for mod in mods_by_status[status]) + "\n"
        
        await ctx.send(msg)

