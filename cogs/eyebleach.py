import requests
from discord.ext import commands

class Faith_In_Humanity(commands.Cog, name='Faith in humanity'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='eyebleach')
    async def eyebleach(self, ctx):
        endpoint = "https://e621.net/posts/random.json?tags=vaporeon+rating:safe+-breasts&limit=10"
        head = {'User-Agent': 'VaporeonBot 1.0.0'}
        r = requests.get(endpoint, headers=head)
        url = r.json().get("post").get("file").get("url")
        try:
            await ctx.send(url)
        except:
            await ctx.send("For whatever reason, *ahem, ahem, check the console* the image couldn't be sent. Sucks to be you, huh?")

def setup(bot):
    bot.add_cog(Faith_In_Humanity(bot))