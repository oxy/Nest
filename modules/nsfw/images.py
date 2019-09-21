import discord
from discord.ext import commands
import nsfw_dl
import nsfw_dl.errors

from nest import exceptions

SERVICES = ["rule34", "e621", "furrybooru", "gelbooru", "konachan", "tbib",
            "xbooru", "yandere"]

def wrap_fn(newname: str, doc: str):
    """
    Decorator which renames a function.
    
    Parameters
    ----------
    newname: str
        Name of the new function.
    doc: str
        Docstring of the new function.
    """
    def decorator(f):
        f.__name__ = newname
        f.__doc__ = doc
        return f
    return decorator

def gen_command(service: str):
    """
    Generates a command helper.
    """
    service_arg = service.capitalize() + 'Search'

    @commands.is_nsfw()
    @commands.command()
    @wrap_fn(service, f"Search {service} for images.")
    async def nsfwsearch(self, ctx, *, query):
        """
        NSFW search utility command, common for every library.
        """
        try:
            content = await self.client.download(service_arg, args=query)
        except nsfw_dl.errors.NoResultsFound:
            raise exceptions.WebAPINoResults(api=service, q=query)
        embed = discord.Embed()
        embed.set_image(url=content)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    return nsfwsearch

class _NSFWCommands:
    def __init__(self, bot):
        self.client = nsfw_dl.NSFWDL(session=bot.session, loop=bot.loop)

for sv in SERVICES:
    setattr(_NSFWCommands, sv, gen_command(sv))

class NSFW(_NSFWCommands, commands.Cog):
    pass
