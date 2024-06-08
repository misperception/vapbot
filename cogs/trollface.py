import discord
from discord.ext import commands
from discord import app_commands
from cogs.lib.vapbotutils import ParseUtils

class VaporeonPorn(commands.Cog, name="Trolling"):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='vapsend', description='[NSFW] Sends a number of Vaporeon images to a target.')
    @app_commands.rename(arg1='user', arg2='number')
    @app_commands.describe(arg1='User to whom DM the images:', arg2='Number of images to DM:')
    async def vapsend(self, ctx, arg1: discord.Member, arg2: int):
        if arg2 <= 0:
            await ctx.send(f"{arg2} is lower or equal to zero.")
            return
        else: pass

        endpoint = "https://e621.net/posts/random.json?tags=Vaporeon+-animated"
        await ctx.send('Sending images...')
        for i in range(arg2):
            try:
                await ParseUtils.EmbedMaker(endpoint,arg1)
            except:
                print(f"couldn't send URL in attempt {i+1}")

    @commands.hybrid_command(name='vappost', description='[NSFW] Posts a number of Vaporeon images to the current channel.')
    @app_commands.rename(arg='number')
    @app_commands.describe(arg='Number of images to post:')
    async def vappost(self, ctx, arg: int):
        if not ctx.channel.is_nsfw(): 
            await ctx.send("Make sure to run this command on a NSFW channel.")
            return
        else: pass

        if arg <= 0:
            await ctx.send("Argument is lower or equal to zero, please choose a positive integer.")
            return
        else: pass

        endpoint = "https://e621.net/posts/random.json?tags=Vaporeon+-animated"
        for i in range(arg):
            try:
                await ParseUtils.EmbedMaker(endpoint,ctx)
            except:
                print(f"couldn't send url in attempt {i+1}")

async def setup(bot):
    await bot.add_cog(VaporeonPorn(bot))