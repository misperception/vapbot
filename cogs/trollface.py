import requests, discord
from discord.ext import commands

class VaporeonPorn(commands.Cog, name="Trolling"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='vapsend')
    async def vapsend(self, ctx, arg1: discord.Member, arg2: int):
        if arg2 <= 0:
            await ctx.channel.send(f"{arg2} is lower or equal to zero.")
            return
        else: pass

        endpoint = "https://e621.net/posts/random.json?tags=Vaporeon+-animated"
        head = {'User-Agent': 'VaporeonBot 1.0.0'}

        for i in range(arg2):
            r = requests.get(endpoint, headers=head)
            url = r.json().get("post").get("file").get("url")
            try:
                await arg1.send(url)
            except:
                print(f"couldn't send URL in attempt {i+1}")

    @commands.command(name='vappost')
    async def vappost(self, ctx, arg: int):
        if not ctx.channel.is_nsfw(): 
            await ctx.send("Make sure to run this command on a NSFW channel.")
            return
        else: pass

        if arg <= 0:
            await ctx.channel.send("Argument is lower or equal to zero, please choose a positive integer.")
            return
        else: pass

        endpoint = "https://e621.net/posts/random.json?tags=Vaporeon+-animated"
        head = {'User-Agent': 'VaporeonBot 1.0.0'}

        for i in range(arg):
            r = requests.get(endpoint, headers=head)
            url = r.json().get("post").get("file").get("url")
            try:
                await ctx.channel.send(url)
            except:
                print(f"couldn't send url in attempt {i+1}")

async def setup(bot):
    await bot.add_cog(VaporeonPorn(bot))