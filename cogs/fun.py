import random, requests, time
from discord.ext import commands
with open("copypasta.txt",'r', encoding='utf-8') as texten:
  copypasta = texten.read()
with open("copypastaes.txt",'r', encoding='utf-8') as textes:
  copypastaes = textes.read()

class Fun(commands.Cog):
    def __init__(bot, self):
        self.bot = bot
    @commands.command(name='roulette')
    async def roulette(self, ctx):
        if ctx.channel.is_nsfw():
            shot = random.randrange(1,7)
            print(f"shot = {shot}")
            if shot < 6:
                await ctx.channel.send("You fired a blank, you are safe now.")
            elif shot == 6:
                await ctx.channel.send("You fired a shot, you lose, prepare for the second roulette.")
                time.sleep(1)
                await ctx.channel.send("Preparing second roulette...")
                time.sleep(2)
                roundtwo = random.randrange(1,7)
                print(f"roundtwo = {roundtwo}")
                if roundtwo < 6:
                    await ctx.channel.send("You fired a blank, loading normal porn...")
                    baseURL = "https://e621.net/posts.json?page={page}&limit=10&tags=-animated+rating:explicit+-vore+-anal_vore+-urine+-feces+-diaper"
                    endpoint = baseURL.format(page = str(random.randrange(1,201)))
                    head = {'User-Agent': 'VaporeonBot 1.0.0'}
                    r = requests.get(endpoint, headers=head)
                    jsonpage = r.json()
                    posts = jsonpage['posts']
                    currentpost = posts[0]
                    file = currentpost['file']
                    url = file['url']
                    time.sleep(2)
                    try:
                        await ctx.send(url)
                    except:
                        for n in range(len(posts)):
                            print("url does not exist")
                            currentpost = posts[n]
                            file = currentpost['file']
                            url = file['url']
                            if url != None:
                                break
                        try:  
                            await ctx.channel.send(url)
                            print("safeguard mechanisms activated at round one")
                        except:
                            ctx.channel.send("The bullet got stuck! Lucky!")

                elif roundtwo == 6:
                    await ctx.channel.send("You fired a shot, loading degeneracy... hope you still have faith in humanity after this...")
                    baseURL = "https://e621.net/posts.json?page={page}&limit=10&tags={tags}&-animated"
                    tag = ["watersports", "omorashi", "scat", "gore", "vore", "anal_prolapse", "anal_vore", "diaper", "intersex+breasts", "ear_penetration"]
                    randomn = random.randrange(1,len(tag))
                    endpoint = baseURL.format(page = str(random.randrange(1,201)), tags = tag[randomn - 1])
                    head = {'User-Agent': 'VaporeonBot 1.0.0'}
                    r = requests.get(endpoint, headers=head)
                    jsonpage = r.json()
                    posts = jsonpage['posts']
                    currentpost = posts[0]
                    file = currentpost['file']
                    url = file['url']
                    time.sleep(1)
                    await ctx.channel.send("Brace for impact.")
                    time.sleep(2)
                    try:
                        await ctx.send(url)
                    except:
                        for n in range(len(posts)):
                            print("url does not exist")
                            currentpost = posts[n]
                            file = currentpost['file']
                            url = file['url']
                            if url != None:
                                break
                        try:  
                            await ctx.channel.send(url)
                            print("safeguard mechanisms activated at round two")
                        except:
                            ctx.channel.send("The bullet got stuck! Lucky!")
        else:
            await ctx.channel.send("Make sure to run this command on a NSFW channel.")

    @commands.command(name='vapcopy')
    async def copyp(self, ctx):
        await ctx.channel.send(copypasta)

    @commands.command(name='vapcopyes')
    async def copypes(self, ctx):
        await ctx.channel.send(copypastaes)

def setup(bot):
    bot.add_cog(Fun(bot))