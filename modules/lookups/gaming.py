"""
Gaming-related lookup commands.
"""

from io import BytesIO

import discord
from discord.ext import commands

from nest import exceptions

URL_MCUUID_API = "https://api.mojang.com/users/profiles/minecraft/{user}"
URL_MCSKIN_API = "https://visage.surgeplay.com/{image}/{uuid}.png"

class GamingLookups:
    category = "user"

    @commands.command()
    async def mcskin(self, ctx, user: str, image: str = "full"):
        url = URL_MCUUID_API.format(user=user)
        
        # Mojang API returns empty response instead of 404 :(
        async with ctx.bot.session.get(url) as resp:
            if resp.status == 204:
                uuid = None
            else:
                uuid = (await resp.json())["id"]
        
        if not uuid:
            await ctx.send(ctx._("mc_usernotfound").format(user))
            return
        
        url = URL_MCSKIN_API.format(image=image, uuid=uuid)

        async with ctx.bot.session.get(url) as resp:
            if resp.status == 200:
                image = BytesIO(await resp.read())
            else:
                raise exceptions.WebAPIInvalidResponse(api="surgeplay", status=resp.status)

        await ctx.send(file=discord.File(fp=image, filename=f"{uuid}.png"))


