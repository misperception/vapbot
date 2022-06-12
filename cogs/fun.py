from ast import Not
import random, requests, time
from discord.ext import commands
with open("copypasta.txt",'r', encoding='utf-8') as texten:
  copypasta = texten.read()
with open("copypastaes.txt",'r', encoding='utf-8') as textes:
  copypastaes = textes.read()
head = {'User-Agent': 'VapBot 1.2.0'}

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
                    endpoint = "https://e621.net/posts.json?tags=-animated+rating:explicit+-vore+-anal_vore+-urine+-feces+-diaper"
                    r = requests.get(endpoint, headers=head)
                    jsonpage = r.json()
                    posts = jsonpage['posts']
                    currentpost = posts[random.randint(0,len(posts)-1)]
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
                    baseURL = "https://e621.net/posts.json?tags={tags}+-animated"
                    tag = ["watersports", "omorashi", "scat", "gore", "vore", "anal_prolapse", "anal_vore", "diaper", "intersex+breasts", "ear_penetration"]
                    randomn = random.randrange(1,len(tag))
                    endpoint = baseURL.format(tags = tag[randomn - 1])
                    r = requests.get(endpoint, headers=head)
                    jsonpage = r.json()
                    posts = jsonpage['posts']
                    currentpost = posts[random.randint(0,len(posts)-1)]
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

    @commands.command(name='vapthird')
    async def oneinthree(self, ctx, tag='none'):
        if not ctx.channel.is_nsfw(): # terminates command if not in a NSFW channel
            await ctx.channel.send('Make sure to run this command on a NSFW channel.')
            return
        value = random.randint(1,3)
        tags = ''
        # executes code based on output number
        dict_rating = {
            1: 'safe',
            2: 'questionable',
            3: 'explicit',
        }
        tags = dict_rating.get(value)
        dict_tag = { # available tags (more may be added in the future)
            'none': "",
            'vap' or 'vaporeon': "+vaporeon",
            'esp' or 'espeon': "+espeon",
            'umbreon': "+umbreon",
            'flareon': "+flareon",
            'jolt' or 'jolteon': "+jolteon",
            'sylveon': "+sylveon",
            'leaf' or 'leafeon': "+leafeon",
            'glaceon': "+glaceon",
            'eevee': "+eevee",
            'eeveelution': "+eeveelution",
            'poke' or 'pokemon': "+pokémon"
        }
        try:
            tags = tags + dict_tag.get(tag) # addition of dict_tag tags according to the argument provided (if at all)
        except:
            if tag != 'help':
                await ctx.channel.send(f'{tag} is not a valid tag, please make sure you are using one of the valid tags')
                return
            else:
                await ctx.send('Tags:')
                await ctx.send(f'``{dict_tag}``')
                return
        endpoint = f'https://e621.net/posts.json?tags=rating%3A{tags}'
        page = requests.get(endpoint, headers=head).json()
        posts = page['posts']
        currentpost = posts[random.randint(0, len(posts) - 1)]
        file = currentpost['file']
        url = file['url']
        await ctx.send(url)   


def setup(bot):
    bot.add_cog(Fun(bot))