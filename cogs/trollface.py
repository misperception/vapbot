import requests, random, discord
from discord.ext import commands

class VaporeonPorn(commands.Cog, name="Trolling"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='vapsend')
    async def vapsend(self, ctx, arg1: discord.Member, arg2):
        if int(arg2) <= 0:
            await ctx.channel.send("The second argument is lower or equal to zero.")
        elif int(arg2) > 100:
            await ctx.channel.send("The second argument is higher than 100, please choose a lower number")
        else:
            baseURL = "https://e621.net/posts.json?tags=Vaporeon+-animated&limit={number}&page={page}"
            endpoint = baseURL.format(number = arg2, page = str(random.randrange(1,201)))
            head = {'User-Agent': 'VaporeonBot 1.0.0'}
            r = requests.get(endpoint, headers=head)
            jsonpage = r.json()
            posts = jsonpage['posts']
            n = len(posts)
            for index in range(n):
                print(index + 1)
                currentpost = posts[index]
                file = currentpost['file']
                url = file['url']
                try:
                    await arg1.send(url)
                except:
                    print("couldn't send URL")

    @commands.command(name='vappost')
    async def vappost(self, ctx, arg):
        if not ctx.channel.is_nsfw(): # exit clause
            await ctx.send("Make sure to run this command on a NSFW channel.")
            return

        try:
            int(arg)
        except:
            await ctx.channel.send("Argument is not a valid number.")
            return
        if int(arg) <= 0:
            await ctx.channel.send("Argument is lower or equal to zero, please choose a positive integer.")
            return
        baseURL = "https://e621.net/posts.json?tags=Vaporeon+-animated&limit={number}"
        endpoint = baseURL.format(number = arg)
        head = {'User-Agent': 'VaporeonBot 1.0.0'}
        r = requests.get(endpoint, headers=head)
        jsonpage = r.json()
        posts = jsonpage['posts']
        n = len(posts)
        for index in range(n):
            print(index + 1)
            currentpost = posts[index]
            file = currentpost['file']
            url = file['url']
            try:
                await ctx.channel.send(url)
            except:
                print("couldn't send url")

def setup(bot):
    bot.add_cog(VaporeonPorn(bot))