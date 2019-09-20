from discord.ext import commands

class AdminCommands(commands.Cog):
    @commands.is_owner()
    @commands.group()
    async def module(self, ctx):
        pass
        
    @module.command()
    async def reload(self, ctx, module: str):
        ctx.bot.reload_module(module)
        await ctx.send(f"Successfully reloaded {module}!")
    
    @commands.is_owner()
    @module.command()
    async def load(self, ctx, module: str):
        ctx.bot.load_module(module)
        await ctx.send(f"Successfully loaded {module}!")
