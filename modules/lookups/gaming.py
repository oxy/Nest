"""
Gaming-related lookup commands.
"""

from io import BytesIO

import discord
from discord.ext import commands
from pycountry import countries

from nest import exceptions

URL_MCUUID_API = "https://api.mojang.com/users/profiles/minecraft/{user}"
URL_MCSKIN_API = "https://visage.surgeplay.com/{image}/{uuid}.png"
URL_OSU_API = "https://osu.ppy.sh/api/get_user"

class GamingLookups(commands.Cog):
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

    @commands.command()
    async def osu(self, ctx, user: str):
        query = {"k": ctx.bot.tokens["osu"], "u": user}

        async with ctx.bot.session.get(URL_OSU_API, params=query) as response:
            if response.status == 200:
                data = await response.json()
            else:
                return

        user = data[0]

        keys = {
            ctx._('Play Count'): 'playcount',
            ctx._('Country'): 'country',
            ctx._('Level'): 'level',
            ctx._('Ranked Score'): 'ranked_score',
            ctx._('Total Score'): 'total_score',
            ctx._('Accuracy'): 'accuracy',
            ctx._('{level} Ranking'.format(level='SS')): 'count_rank_ss',
            ctx._('{level} Ranking'.format(level='S')): 'count_rank_s',
            ctx._('{level} Ranking'.format(level='A')): 'count_rank_a',
            '300s': 'count300',
            '100s': 'count100',
            '50s': 'count50'
        }

        userid = user['user_id']
        username = user['username']

        embed = discord.Embed(title=username, description=userid, url=f"https://osu.ppy.sh/u/{userid}")

        # Convert some data in the dict before iterating through it
        user['accuracy'] = round(float(user['accuracy']), 2)
        user['country'] = countries.get(alpha_2='PH').name

        for field, value in keys.items():
            embed.add_field(name=field, value=user[value], inline=True)

        embed.set_thumbnail(url=f"http://a.ppy.sh/{userid}")
        await ctx.send(embed=embed)

