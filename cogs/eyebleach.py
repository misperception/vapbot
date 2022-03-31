import requests, random
from discord.ext import commands

class Faith_In_Humanity(commands.Cog, name='Faith in humanity'):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='eyebleach')
    async def eyebleach(self, ctx):
        baseURL = "https://e621.net/posts.json?page={page}&tags=vaporeon+rating:safe+-breasts&limit=10"
        endpoint = baseURL.format(page = str(random.randrange(1,30)))
        head = {'User-Agent': 'VaporeonBot 1.0.0'}
        r = requests.get(endpoint, headers=head)
        jsonpage = r.json()
        posts = jsonpage['posts']
        currentpost = posts[0]
        file = currentpost['file']
        url = file['url']
        try:
            await ctx.send(url)
        except:
            for n in range(len(posts)):
                currentpost = posts[n]
                file = currentpost['file']
                url = file['url']
                if url != None:
                    break
            try:
                await ctx.channel.send(url)
            except: return

def setup(bot):
    bot.add_cog(Faith_In_Humanity(bot))