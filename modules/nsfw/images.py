import discord
from discord.ext import commands
import nsfw_dl

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.client = nsfw_dl.NSFWDL(session=bot.session, loop=bot.loop)

    @commands.is_nsfw()
    @commands.command()
    async def rule34(self, ctx, *, query):
        content = await self.client.download('Rule34Search', args=query)
        embed = discord.Embed()
        embed.set_image(url=content)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    async def e621(self, ctx, *, query):
        content = await self.client.download('E621Search', args=query)
        embed = discord.Embed()
        embed.set_image(url=content)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    async def furrybooru(self, ctx, *, query):
        content = await self.client.download('FurrybooruSearch', args=query)
        embed = discord.Embed()
        embed.set_image(url=content)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    async def gelbooru(self, ctx, *, query):
        content = await self.client.download('GelbooruSearch', args=query)
        embed = discord.Embed()
        embed.set_image(url=content)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    async def konachan(self, ctx, *, query):
        content = await self.client.download('KonachanSearch', args=query)
        embed = discord.Embed()
        embed.set_image(url='http:'+content)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    async def tbib(self, ctx, *, query):
        content = await self.client.download('TbibSearch', args=query)
        embed = discord.Embed()
        embed.set_image(url=content)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    async def xbooru(self, ctx, *, query):
        content = await self.client.download('XbooruSearch', args=query)
        embed = discord.Embed()
        embed.set_image(url=content)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    async def yandere(self, ctx, *, query):
        content = await self.client.download('YandereSearch', args=query)
        embed = discord.Embed()
        embed.set_image(url=content)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

